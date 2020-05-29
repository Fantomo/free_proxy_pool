# -*- encoding:utf-8 -*-

import os
import yaml


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yml')
TOOLS_PATH = os.path.join(BASE_PATH, 'tools')


class YamlReader:

	def __init__(self, yaml_file_path):
		if os.path.exists(yaml_file_path):
			self.yaml_file_path = yaml_file_path
		else:
			raise FileNotFoundError("文件未找到！")
		self._data = None

	@property
	def data(self):
		if not self._data:
			with open(self.yaml_file_path, 'rb') as f:
				self._data = list(yaml.safe_load_all(f))

			return self._data


class Config:

	def __init__(self, config=CONFIG_FILE):
		self.config = YamlReader(config).data

	def get(self, key, index=0):
		return self.config[index].get(key)
