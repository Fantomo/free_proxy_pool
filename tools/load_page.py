# -*- encoding: utf-8 -*-

import requests
import random

from tools.config import Config

class Spider:

	def __init__(self, url=None, method='GET', data=None, params=None):
		self._url = url
		self._method = method
		self._data = data
		self._params = params
		self._header = random.choice(Config().get('user-anger'))


	@property
	def get(self):
		response = requests.get(self._url, headers=self._header, params=self._params)
		return response.content

	@property
	def post(self):
		response = resquests.post(self._url, headers=self._header, data=self._data, params=self._params)
		return response.content
