# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging
import traceback


class HudongbaikePipeline(object):
	def __init__(self):
		self.conn = pymysql.connect(host = 'localhost',
			port = 3306,
			user = 'root',
			password = '',
			db = '',
			charset = 'utf8mb4')
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		sql = """insert into record
		(url, place, title, prefix)
		values
		("%s", "%s", "%s", "%s");
		"""
		URL = item['URL']
		Place = item['Place']
		Title = item['Title']
		Prefix = item['Prefix']
		#sql = sql.format(URL, Place, Title, Prefix)
		try:
			self.conn.ping(reconnect = True)  # 防止连接断开
			self.cursor.execute(sql, [URL, Place, Title, Prefix])
			self.conn.commit()
		except:
			traceback.print_exc()
		return item

	def close_spider(self, spider):
		self.conn.close()