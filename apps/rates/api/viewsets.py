import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.tokeninfo.models import Token, TokenInfo, TokenUsage


class RatesView(APIView):
    renderer_classes = [JSONRenderer]
    banxico_url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno?token='
    banxico_url += settings.BANXICO_TOKEN
    DOF_url = 'https://www.dof.gob.mx/indicadores_detalle.php?cod_tipo_indicador=158&dfecha='
    fixer_url = 'http://data.fixer.io/api/latest?symbols=MXN&access_key=' + settings.FIXER_ACCESS_KEY  # + '&base=USD'

    def get_rates(self, token=None):

        if token is None:
            content = {'Error': "No Token Provided"}
            return content

        if Token.objects.filter(key=token).count() < 1:
            content = {'Error': "Not Valid Token"}
            return content

        token_info = TokenInfo.objects.filter(token=token).first()
        today_date = datetime.now().date()
        today_token_usage = TokenUsage.objects.filter(token_info=token_info, date=today_date).count()

        if today_token_usage >= token_info.limit_usage:
            content = {'Error': "Exceeded Daily Limit Usage",
                       'limit_usage': str(token_info.limit_usage)}
            return content
        token_usage = TokenUsage(token_info=token_info, date=today_date)
        token_usage.save()

        content = {'rates': {}}

        # Banxico
        banxico_request = requests.get(self.banxico_url)
        bmx_content = json.loads(banxico_request.content)
        bmx_data = bmx_content['bmx']['series'][0]['datos']
        bmx_dict = {
            'Banxico': {
                'value': bmx_data[0]['dato'],
                'last_updated': bmx_data[0]['fecha'].replace('/', '-',),
            },
        }
        content['rates'].update(bmx_dict)

        # Diario Oficial de la Federación
        today = datetime.now()
        DOF_date = today.strftime("%d") + '%2F' + today.strftime("%m") + '%2F' + today.strftime("%y")  # 22%2F01%2F2021
        DOF_request = requests.get(self.DOF_url + DOF_date + '&hfecha=' + DOF_date)
        DOF_soup = BeautifulSoup(DOF_request.text)
        DOF_data = DOF_soup.find_all('tr', {'class', 'Celda 1'})[0].find_all('td')
        DOF_dict = {
            'Diario Oficial de la Federación': {
                'rate': DOF_data[1].text[:-2],
                'last_updated': DOF_data[0].text,
            }
        }
        content['rates'].update(DOF_dict)

        # Fixer
        fixer_request = requests.get(self.fixer_url)
        fixer_data = json.loads(fixer_request.content)
        fixer_date = fixer_data['date']
        fixer_dict = {
            'Fixer': {
                'value': str(fixer_data['rates']['MXN'])[:-2],
                'last_updated': fixer_date[8:10] + fixer_date[4:8] + fixer_date[0:4]
            },
        }
        content['rates'].update(fixer_dict)

        return content

    def get(self, request, format=None):
        content = self.get_rates(token=request.GET.get('token'))
        return Response(content)

    def post(self, request, format=None):
        content = self.get_rates(token=request.GET.get('token'))
        return Response(content)
