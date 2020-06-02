# -*- encoding:utf-8 -*-

import redis
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from tools.config import Config

db_config = Config().get('db')
TABLE_NAME = db_config['tablename']

app = Flask(__name__)


# mysql
class DBConfig:

	db_host = db_config['host']
	db_port = db_config['port']
	db_user = db_config['user']
	db_passwd = db_config['passwd']
	database = db_config['database']

	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % (db_user, db_passwd, db_host, db_port, database)
	# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_user, db_passwd, db_host, db_port, database)

	# 暂时解决 sqlalchemy 连接数超过20个时报错问题 
	SQLALCHEMY_POOL_SIZE = 1024

	# 自动提交
	SQLALCHEMY_COMMIT_ON_TEARDOWN = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(DBConfig)
db = SQLAlchemy(app)


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


# 数据入库
def addIp(proto, ip, port):
	ip = IPPool(proto=proto, ip=ip, port=port)
	db.session.add(ip)
	db.session.commit()


# 获取ip
def query_ip(start, count):
	flag = False
	ip_list = IPPool.query.limit(count).offset(start).all()

	# 数据库查到最后一组时重头开始查
	if len(ip_list) == 0:
		ip_list = IPPool.query.limit(count).offset(0).all()
		flag = True
	return ip_list, flag


# redis
class RedisConfig:

	def __init__(self):
		redis_config = Config().get('redis')
		redis_host = redis_config['host']
		redis_port = redis_config['port']

		pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
		self.r = redis.Redis(connection_pool=pool)

	def add_data(self, key, data):
		pipe = self.r.pipeline()
		pipe.sadd(key, data)
		pipe.execute()

	def get_data(self, key):
		return self.r.spop(key)

	def count_data(self, key):
		return self.r.scard(key)

redis_cli = RedisConfig()
