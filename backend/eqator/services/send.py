from django.conf import settings
from ..helpers import print_default
import requests
import json


class SendService:
    url_base = getattr(settings, 'EQATOR_SEND_HOST', None)

    def report(self, *args, **kwargs):
        url_base = self.url_base
        if url_base is None:
            raise ValueError('To send, set EQATOR_SEND_HOST')
        json_data = json.dumps({
            'data': kwargs
        }, indent=4, sort_keys=True, default=str)
        r = requests.post(url_base, data=json_data)
        print_default(f'Send status - {r.status_code}\n')


send_service = SendService()
