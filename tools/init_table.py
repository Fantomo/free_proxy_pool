# -*- encoding:utf-8 -*-
import sys
sys.path.append("..")

from tools.db_tools import db


if __name__ == '__main__':
	db.drop_all()
	db.create_all()
