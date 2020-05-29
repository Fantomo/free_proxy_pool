# -*- encoding:utf-8 -*-

from tools.init_table import IPPool
from tools.db_tools import db

def addIp(proto, ip, port):
	ip = IPPool(proto=proto, ip=ip, port=port)
	db.session.add(ip)
	db.session.commit()