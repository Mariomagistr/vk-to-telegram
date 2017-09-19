import requests
from urllib import request
import urllib
import json
import config

def vkMethod(method, data={}):
	url = 'https://api.vk.com/method/%s.json' % (method)
	data.update({'access_token': config.vkToken})
	data.update({'v':5.68})
	response = requests.post(url, data)
	print(response.status_code)
	response = response.json()
	if 'error' in response:
		print('VK API error: %s' % (response['error']['error_msg']))
		return response
	else:
		return response['response']