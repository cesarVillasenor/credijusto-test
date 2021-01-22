import requests
import json
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class RatesView(APIView):
    renderer_classes = [JSONRenderer]
    banxico_url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno?token='
    banxico_url += settings.BANXICO_TOKEN

    def get_rates(self):
        content = {'rates': {

        }
        }
        banxico_request = requests.get(self.banxico_url)
        bmx_content = json.loads(banxico_request.content)
        bmx_data = bmx_content['bmx']['series'][0]['datos']
        bmx_dict = {
            'Banxico': {
                'value': bmx_data[0]['dato'],
                'last_updated': bmx_data[0]['fecha'],
            },
        }
        content['rates'].update(bmx_dict)

        return content

    def get(self, request, format=None):
        content = self.get_rates()
        return Response(content)

    def post(self, request, format=None):
        content = self.get_rates()
        return Response(content)

