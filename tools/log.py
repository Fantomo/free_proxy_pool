# -*- encoding:utf-8 -*-

import logging

from tools.config import Config, LOGPATH

logconfig = Config().get('log_config')
log_file = LOGPATH + logconfig['file']
log_level = logconfig['level']
pattern = logconfig['pattern']
datefmt = logconfig['datefmt']


class Logger:

	def __init__(self):
		self.logger = logging.basicConfig(
			filename=log_file,
			level=log_level,
			format=pattern,
			datefmt=datefmt)

	def get_logger(self, name):
		self.logger = logging.getLogger(name)
		return self.logger


logger = Logger()
