import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class RatesView(APIView):
    renderer_classes = [JSONRenderer]
    banxico_url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno?token='
    banxico_url += settings.BANXICO_TOKEN
    DOF_url = 'https://www.dof.gob.mx/indicadores_detalle.php?cod_tipo_indicador=158&dfecha='

    def get_rates(self):
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
        return content

    def get(self, request, format=None):
        content = self.get_rates()
        return Response(content)

    def post(self, request, format=None):
        content = self.get_rates()
        return Response(content)
