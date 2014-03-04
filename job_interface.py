#coding: utf8

'''
Created on 2013-10-24
@author: changshuai
'''
from db_operator import *
import common

class JobInterface:
	def init(self, conf):
		self.conf = conf
		self.language = conf.language
		self.db = DBOperator(conf.db_ip, conf.db_port, conf.db_user, conf.db_passwd, conf.db_name, conf.language)
		return self.db.connect()

	def __del__(self):
		if self.db:
			#self.db.close()
			self.db = None

	def run(self):
		pass

