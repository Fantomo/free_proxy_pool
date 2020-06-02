# -*- encoding: utf-8 -*-

import sys
sys.path.append("..")

from tools.log import logger
log = logger.get_logger(__file__)
from spider.spider_common_tools import start_spider_page



def xc_ip_spider():
	log.info("start xici ip spider")
	url = "http://www.xicidaili.com/nn/1"

	"""
	xpath_dict = {
		# IP组xpath 
		"ip_group": "//tbody/tr",
		# ip xpath
		"ip": "./td[1]/text()",
		# 端口 xpath
		"port": "./td[2]/text()",
		# 协议 xpath
		"proto" :"./td[4]/text()"
	}
	"""

	xpath_dict = {
		"ip_group": "//table[@id='ip_list']//tr[@class]",
		"ip": "./td[2]/text()",
		"port": "./td[3]/text()",
		"proto": "./td[6]/text()"
	}

	start_spider_page(req_url=url, xpath_dict=xpath_dict)


def seo_ip_spider():
	log.info("Start seofangfa ip spider")
	url = "https://proxy.seofangfa.com/"
	xpath_dict = {
		"ip_group": "//table[@class='table']/tbody/tr",
		"ip": "./td[1]/text()",
		"port": "./td[2]/text()",
		"proto": ""
	}

	start_spider_page(req_url=url, xpath_dict=xpath_dict)


def kdl_ip_spider():
	log.info("Start kuaidaili ip spider")
	
	xpath_dict = {
		"ip_group": "//tbody/tr",
		"ip": "./td[1]/text()",
		"port": "./td[2]/text()",
		"proto": "./td[4]/text()"
	}

	for page in range(1, 4):
		url = "http://www.kuaidaili.com/free/inha/{}".format(page)
		start_spider_page(req_url=url, xpath_dict=xpath_dict)

if __name__ == '__main__':
	# xc_ip_spider()
	# seo_ip_spider()
	kdl_ip_spider()
