# -*- encoding: utf-8 -*-

import sys
sys.path.append('..')
import json

from lxml import etree

from tools.load_page import Spider
from tools.db_tools import redis_cli
from tools.add_data import addIp
from tools.config import Config

REDIS_KEY = Config().get('redis')['key']


def test(page=1):
	print(page)
	url = "http://www.kuaidaili.com/free/inha/{}".format(page)
	print(url)
	spider = Spider(url=url)
	response = spider.get
	content = etree.HTML(response)
	parse_page(content)

def parse_page(context):
	ip_dict = {}
	ip_lists = context.xpath("//tbody/tr")

	for ip_list in ip_lists:
		ip = ip_list.xpath("./td[1]/text()")[0]
		port = ip_list.xpath("./td[2]/text()")[0]
		proto = ip_list.xpath("./td[4]/text()")[0]

		# ips = proto + "://" + ip + ":" + port
		# addIp(proto, ip, port)
		ip_dict['proto'] = proto
		ip_dict['ip'] = ip
		ip_dict['port'] = port
		redis_cli.add_data(REDIS_KEY, json.dumps(ip_dict))

# 		ip_storage(ips)


# def ip_storage(ips):
# 	with open("ip.txt", "a") as f:
# 		f.write(ips + '\n')


if __name__ == '__main__':
	for i in range(1, 8):
		test(i)