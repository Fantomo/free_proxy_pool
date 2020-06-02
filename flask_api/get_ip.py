# -*- encoding: utf-8 -*-

import sys
sys.path.append("..")
import json
from flask import Flask, request

from tools.db_tools import query_ip

app = Flask(__name__)
start = 0

"""
request url:
	get_free_ip
request method: get
request param:
	action=get_ip: 必选 String
	count: 	必选 String 获取ip的数量 <= 5
返回示例:
	{
	  "result_code": "200",
	  "result_msg": "请求成功",
	  "result": true,
	  "ip_list": [
	    {
	      "proto": "HTTP",
	      "ip": "163.204.245.76",
	      "port": "9999"
	    }
	  ]
	}

返回参数:
	proto: 	代理协议
	ip:		代理ip
	port:	代理端口
"""

@app.route("/get_free_ip", methods=['GET'])
def get_ip_api():
	result = {
		"result_code": "200",
		"result_msg": "请求成功",
		"result": True
	}

	if request.args:
		get_data = request.args.to_dict()
		try:
			action = get_data.get('action')
			count = int(get_data.get('count'))
			if action == 'get_ip' and count <= 5:
				result['ip_list'] = get_ip(count)
				return json.dumps(result, ensure_ascii=False)
			else:
				result['result_code'] = '204'
				result['result_msg'] = '请求参数错误'
				result['result'] = False
				return json.dumps(result, ensure_ascii=False)
		except:
			result['result_code'] = '206'
			result['result_msg'] = '请求参数错误'
			result['result'] = False
			return json.dumps(result, ensure_ascii=False)
	else:
		result['result_code'] = '205'
		result['result_msg'] = '未查询到数据'
		result['result'] = False
		return json.dumps(result, ensure_ascii=False)

# 查询可用ip
def get_ip(count):
	global start

	ips, flag = query_ip(start, count)
	ip_group = []
	for ip in ips:
		ip = {
			"proto": ip.proto,
			"ip": ip.ip,
			"port": ip.port
		}
		ip_group.append(ip)

	if flag:
		start = count
	else:
		start += count

	return ip_group


if __name__ == '__main__':
	app.run(debug=True)
