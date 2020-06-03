# -*- encoding:utf-8 -*-

import time
import logging

from tools.config import Config, LOGPATH

logconfig = Config().get('log_config')
log_file = logconfig['file']
log_level = logconfig['level']
pattern = logconfig['pattern']
datefmt = logconfig['datefmt']

today = time.strftime("%Y%m%d", time.localtime(time.time()))
logfilename = LOGPATH + today + "_" + log_file

class Logger:

	def __init__(self):
		self.logger = logging.basicConfig(
			filename=logfilename,
			level=log_level,
			format=pattern,
			datefmt=datefmt)

	def get_logger(self, name):
		self.logger = logging.getLogger(name)
		return self.logger


logger = Logger()
