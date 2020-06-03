# -*- encoding: utf-8 -*-

import sys
sys.path.append("..")

from tools.log import logger
from tools.db_tools import db
from tools.config import Config
from tools.ip_verify import verify_available_proxy
from flask_api.get_ip import app
from spider.spider_main import start_spider

IS_INIT_DATABASE = Config().get("IS_INIT_DATABASE")
IS_VERIFY = Config().get("is_verify")

log = logger.get_logger(__file__)


if __name__ == '__main__':
	# 收集ip到redis 中
	log.info("Start crawling IP")
	start_spider()
	# 初始化数据库
	if IS_INIT_DATABASE:
		log.info("Start initializing the database")
		db.drop_all()
		db.create_all()
	# 验证ip可用
	if IS_VERIFY:
		log.info("Start validating available IP")
		verify_available_proxy()
	# 开启获取ip 接口
	log.info("Open the request IP interface")
	app.run("0.0.0.0", port="80")
