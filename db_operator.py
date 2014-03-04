#coding: utf8

import time, MySQLdb, ConfigParser
import common
import urlparse

class MyException(Exception):
	__data = ""
	def __init__(self,data):
		self.__data = data
	def __str__(self):
		return self.__data


class SiteDict:
	def __init__(self):
		self.filename = '' 
		self.dict = {}
	def load(self, filename):
		file_object = open(filename, 'rb')
		try:
		    while True:
				line = file_object.readline()
				if not line:
					break
				(site, priority) = line.strip().split(' ')
				site = site.strip()
				priority = int(priority.strip())
				self.dict[site] = priority
		except Exception as e:
			print e.message
			print "error"
			#common.logger.error("DictSet load error:%s" % (e.message))
		finally:
			file_object.close( )

		#common.logger.info("total %d site priority in sitedict:%s" % (len(self.dict), filename))
		return 0

	def get_priority(self, url):
		if url[0:7] == 'http://':
			url = url[7:-1]
		elif url[0:8] == 'https://':
			url = url[8:-1]
		if url[0:4] != 'www.':
			url = 'www.' + url
		url = 'http://' + url
		site = urlparse.urlparse(url).netloc
		if site in self.dict:
			#common.logger.info("url:%s site:%s priority:%d" % (url, site, self.dict[site]))
			return self.dict[site]
		#common.logger.info("url:%s site:%s priority:%d,dictsize:%d" % (url, site, 0, len(self.dict)))
		return 0

class MyConf:
	def __init__(self, filename):
		self.filename = filename
		self.site_dict = SiteDict()

	def parse(self):
		parser = ConfigParser.ConfigParser()
		parser.read(self.filename)
		self.language = parser.get('SERVERS', 'language').strip().rstrip('/')
		if self.language != 'th' and self.language != 'br' and self.language != 'ar':
			common.logger.error("parse SERVERS.language illegal: %s not match[th|ar|br]" % (self.language))
			return -1

		self.db_ip = parser.get('SERVERS', self.language + '_host')
		self.db_port = parser.getint('SERVERS', self.language + '_port')
		self.db_user = parser.get('SERVERS', self.language + '_user')
		self.db_passwd = parser.get('SERVERS', self.language + '_passwd')
		self.db_name = parser.get('SERVERS', self.language + '_db')
		self.log_file = parser.get('LOG', 'log_file')
		self.log_level = parser.get('LOG', 'log_level')

		self.db_description_table = parser.get('TABLE', self.language + '_description')
		self.db_relation_table = parser.get('TABLE', self.language + '_relation')
		self.db_link_table = parser.get('TABLE', self.language + '_link')

		self.task_num = parser.getint('JOB', 'task_num')

		if self.task_num > 0:
			self.task1_is_open = parser.getint('JOB', 'task1_is_open')
			if self.task1_is_open:
				self.task1_name = parser.get('JOB', 'task1_name')
				self.task1_result_limit = parser.getint('JOB', 'task1_result_limit')
				self.task1_excel_output = parser.getint('JOB', 'task1_excel_output')
				self.task1_xml_output = parser.getint('JOB', 'task1_xml_output')
				self.task1_output_dir = parser.get('JOB', 'task1_output_dir').strip()

		if self.task_num > 1:
			self.task2_is_open = parser.getint('JOB', 'task2_is_open')
			if self.task2_is_open:
				self.task2_name = parser.get('JOB', 'task2_name')
	
		if self.task_num > 2:
			self.task3_is_open = parser.getint('JOB', 'task3_is_open')
			if self.task3_is_open:
				self.task3_name = parser.get('JOB', 'task3_name')
				self.str_fields = parser.get('JOB', 'task3_str_fields')
				self.int_fields = parser.get('JOB', 'task3_int_fields')


		self.site_dict_file = parser.get('JOB', self.language + '_site_dict')
		self.site_dict.load(self.site_dict_file)

		self.tool_path = parser.get('JOB', 'tool_path')
		self.thumbnail_process = parser.getint('JOB', 'thumbnail_process')

		return 0

class DBOperator:
	def __init__(self, ip, port, user, passwd, name, language):
		self.db_ip = ip
		self.db_port = port
		self.db_user = user
		self.db_passwd = passwd
		self.db_name = name
		self.language = language
		self.conn = None
	
	def __del__(self):
		if self.conn:
			#self.conn.commit()
			self.conn.close()

	def connect(self):
		try:
			self.conn = MySQLdb.connect(host=self.db_ip, port=self.db_port, user=self.db_user,passwd=self.db_passwd, charset="utf8")  
			self.conn.select_db(self.db_name)
		except MySQLdb.Error, e:
			common.logger.warn("mysql connect to %s:%d error:%d:%s" % (self.db_ip, self.db_port, e.args[0], e.args[1]))
			return -1
		print "conn sccuess to %s:%d, user:%s, db_name:%s" % (self.db_ip, self.db_port, self.db_user, self.db_name)
		return 0

	def query(self, sql):
		result = None
		rows = -1
		cursor = self.conn.cursor()
		try:
			rows = cursor.execute(sql)    
			result = cursor.fetchall()
		except MySQLdb.Error, e:
			common.logger.warn("mysql query error:%d:%s" % (e.args[0], e.args[1]))

		cursor.close()
		return (rows, result)

#def close(self):
#		self.conn.close()


