import requests
from urllib import request
import urllib
import json
import config

TToken = config.TToken

def TMethod(method, data={}):
    try:
        url = 'https://api.telegram.org/bot{}/{}'.format(TToken, method)
        response = requests.post(url, data)
        print(response.status_code)
        response = response.json()
        if 'error' in response:
            print('Telegram API error: %s' % (response['error']['error_msg']))
            return response
        else:
            for i in response:
                print(i)
    except:
        print('error')