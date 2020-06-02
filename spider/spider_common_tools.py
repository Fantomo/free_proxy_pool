# -*- encoding:utf-8 -*-

import sys
sys.path.append('..')
import json
import random
import requests

from lxml import etree

from tools.db_tools import redis_cli, addIp
from tools.config import Config
from tools.log import logger

log = logger.get_logger(__file__)


REDIS_KEY = Config().get('redis')['key']
# 是否开启ip验证
IS_VERIFY = Config().get("is_verify")


class Spider:

	def __init__(self, url=None, data=None, params=None):
		self._url = url
		self._data = data
		self._params = params
		self._header = random.choice(Config().get('user-angers'))
		"""
        constructor for Spider
        :param _url: String, request url
        :param _data: dict, post 参数 
        :param _params: 
        """


	# 使用get请求
	@property
	def get(self):
		response = requests.get(self._url, headers=self._header, params=self._params)
		return response.content

	# 使用post请求
	@property
	def post(self):
		response = resquests.post(self._url, headers=self._header, data=self._data, params=self._params)
		return response.content


# 爬取整页
def start_spider_page(req_url, req_data=None, req_params=None, req_method='GET', xpath_dict=None):
	spider = Spider(url=req_url, data=req_data, params=req_params)
	if req_method.upper() == 'GET':
		content = etree.HTML(spider.get)
	elif req_method.upper() == 'POST':
		content = etree.HTML(spider.port)
	spider_parse_page(content, xpath_dict)

# 解析数据
def spider_parse_page(content, xpath_dict):
	"""
	xpath_dict = {
		ip_group:"//tbody/tr",
		ip:"./td[1]/text()",
		port:"./td[2]/text()",
		proto:"./td[4]/text()"
	}
	"""
	index_xpath = xpath_dict['ip_group']
	ip_xpath = xpath_dict['ip']
	port_xpath = xpath_dict['port']
	proto_xpath = xpath_dict['proto']


	ip_dict = {}
	ip_lists = content.xpath(index_xpath)

	for ip_list in ip_lists:
		ip = ip_list.xpath(ip_xpath)[0]
		port = ip_list.xpath(port_xpath)[0]
		proto = ip_list.xpath(proto_xpath)[0] if proto_xpath else "http"

		# 开启验证后数据先存入redis
		if IS_VERIFY:
			ip_dict['proto'] = proto
			ip_dict['ip'] = ip
			ip_dict['port'] = port
			redis_cli.add_data(REDIS_KEY, json.dumps(ip_dict))
		else:
			# 不验证IP是否可用, 直接存入数据库
			addIp(proto, ip, port)
