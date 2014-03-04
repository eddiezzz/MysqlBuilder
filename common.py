#coding: utf8

'''
Created on 2013-10-24
@author: changshuai
'''
import logging
import time
import urllib
import poster
import string
import random
import threading
import json
import pdb
import sys, os
import httplib2

reload(sys) 
sys.setdefaultencoding('utf8')

logger = None

def init_log(log_file, level):
	global logger
	logger = logging.getLogger('sonny')
	hdlr = logging.FileHandler(log_file)
	formatter = logging.Formatter('%(asctime)s %(levelname)s [%(module)s:%(funcName)s:%(lineno)d] %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	set_level = logging.INFO
	if level == 'DEBUG':
		set_level = logging.DEBUG
	elif level == 'WARN':
		set_level = logging.WARN

	logger.setLevel(set_level)

class HttpClient:
	@staticmethod
	def GET(url):
		resp, content = httplib2.Http().request(url, "GET")
		return content 

class Extractor:
	@staticmethod
	def json_extract(keys, result):
		obj = json.loads(result, encoding='utf-8')
		if not obj:
			return "json-error"

		result = ''
		for key in keys:
			if not obj[key]:
				result += 'None'
			elif type(obj[key]) == type(u'string'):
				result = result + obj[key].encode('utf8')
			elif type(obj[key] == type(1)):
				result = result + str(obj[key])
			else:
				result = result + json.JSONEncoder().encode(obj[key]).encode('utf8')
			result += ' '
		return result

def timestamp_to_string(stamp):  
	return time.strftime("%Y", time.localtime(stamp)) 
