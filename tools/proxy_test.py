# -*- encoding:utf-8 -*-

import sys
sys.path.append("..")
import json
import requests

from tools.db_tools import redis_cli, addIp
from tools.config import Config
from tools.log import logger

REDIS_KEY = Config().get('redis')['key']
TEST_URL = Config().get("test_proxy_url")
log = logger.get_logger(__file__)



def get_ip():
	count = redis_cli.count_data(REDIS_KEY)
	if count:
		tmp_ip = json.loads(redis_cli.get_data(REDIS_KEY))
		proto = tmp_ip['proto']
		ip = tmp_ip['ip']
		port = tmp_ip['port']
		return proto, ip, port, count
	else:
		log.warning("No data in redis")
		raise NoDataInCache("redis中没有数据")

class NoDataInCache(Exception):
	pass


def verify_available_proxy():

	flag = True
	while flag:
		proto, ip, port, count = get_ip()
		if count == 1:
			flag = False
		try:
			# 验证代理是否可用
			response = requests.get(TEST_URL, proxies={proto:"{}://{}:{}".format(proto, ip, port)}, timeout=5)
			# 验证可用后存入redis
			addIp(proto, ip, port)
			log.info("%s :Agent available" % ip)

		except:
			log.info("%s :Agent is not available" % ip)


if __name__ == '__main__':
	verify_available_proxy()
