# -*- encoding:utf-8 -*-

import datetime

from tools.db_tools import db
from tools.config import Config

TABLE_NAME = Config().get('db')['tablename']

# ip数据表
class IPPool(db.Model):
	__tablename__ = TABLE_NAME

	id = db.Column(db.Integer, primary_key=True)
	proto = db.Column(db.String(8), comment="协议")
	ip = db.Column(db.String(64), comment="ip地址")
	port = db.Column(db.String(8), comment="端口")
	proofTime = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False, comment="验证时间")

	def __repr__(self):
		return "ip:%s://%s:%s" % (self.proto, self.ip, self.port)


if __name__ == '__main__':
	db.drop_all()
	db.create_all()
