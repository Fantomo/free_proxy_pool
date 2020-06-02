# -*- encoding: utf-8 -*-

import sys
sys.path.append("..")
import json
from flask import Flask, request

from tools.db_tools import query_ip

app = Flask(__name__)
start = 0


@app.route("/", methods=['GET'])
def get_ip():
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
				result['ip_list'] = ip(count)
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


def ip(count):
	init_count = count
	global start

	ips = query_ip(start, count, init_count)
	ip_group = []
	for ip in ips:
		ip = {
			"proto": ip.proto,
			"ip": ip.ip,
			"port": ip.port
		}
		ip_group.append(ip)

	if len(ip_group) < count:
		start = 0
	else:
		start += count
	return ip_group


if __name__ == '__main__':
	app.run(debug=True)
