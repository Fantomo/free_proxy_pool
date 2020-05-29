# -*- encoding:utf-8 -*-

import sys
sys.path.append("..")
import json
import requests

from tools.db_tools import redis_cli
from tools.add_data import addIp
from tools.config import Config

REDIS_KEY = Config().get('redis')['key']
TEST_URL = Config().get("test_proxy_url")

def get_ip():
	tmp_ip = json.loads(redis_cli.get_data(REDIS_KEY))
	proto = tmp_ip['proto']
	ip = tmp_ip['ip']
	port = tmp_ip['port']
	return proto, ip, port, redis_cli.count_data(REDIS_KEY)

def verify_available_proxy():
	proto, ip, port, count = get_ip()
	if count:
		try:
			# response = requests.get(TEST_URL, proxies={"http":"http://223.242.224.37:9999"}, timeout=10)
			print("{}://{}:{}".format(proto, ip, port))
			response = requests.get(TEST_URL, proxies={proto:"{}://{}:{}".format(proto, ip, port)}, timeout=5)
			addIp(proto, ip, port)
			print("代理可用")
			# print(response.content)

		except:
			print("代理不可用")

if __name__ == '__main__':
	proto, ip, port, count = get_ip()
	while count:
		verify_available_proxy()
