#!coding=utf8

from IPy import *
from config import *
import requests
import time
import json

class TransTopoModel(object):
	
	# 获取指定域名，在最近几天内所有通信对端的拓扑网络
	async def get_max_topo(self, ips, length):

		node = []
		resolve = ips
		opposite = []
		link = []

		# 取有记录的日期里，最近length天
		proxy = IPCIS_CONFIG
		url_tables = "http://211.65.197.210:8080/IPCIS/activityDatabase/?Mode=3"
		r_tables = requests.get(url_tables, proxies=proxy)
		tables = r_tables.json()["tables"][-length:]

		for date in tables:
			for ip in ips:
				url = "http://211.65.197.210:8080/IPCIS/activityDatabase/?IpSets=%s:32&TableName=%s&Mode=1" % (ip, date)
				r = requests.get(url, proxies=proxy)
				try:
					res = r.json()[ip+":32"]
				except:
					continue
				# 只统计以目标IP为宿地址的流记录
				for i in res[1][1:]:
					src = i.split(" ")[0]
					dst = i.split(" ")[1]
					if dst not in opposite:
						opposite.append(dst)
						link.append({"source": resolve.index(src), "target": opposite.index(dst) + len(resolve)})

		resolve.extend(opposite)
		for index, item in enumerate(resolve):
			node.append({"id": index, "name": item})

		return {"nodes": node, "links": link}
	