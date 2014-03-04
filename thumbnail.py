#coding: utf8

import os,sys
import codecs
import common
import time

class GipsResulsParser:
	@staticmethod
	def parse(line):
		tn_url = line.split(' ')[4]#.lstrip('tn_url[').rstrip(']') 
		objurl = line.split(' ')[0]
		if tn_url.find('tn_url') == -1:
			tn_url = None
		else:
			tn_url = tn_url.lstrip('tn_url[').rstrip(']')
		if objurl.find('objurl') == -1:
			objurl = None
		else:
			objurl = objurl.lstrip('objurl[').rstrip(']')
		return (objurl, tn_url)


class ThumbnailOperator:
	def __init__(self, tool_path):
		self.tn_dict = {}
		if not (os.path.exists(tool_path) and os.path.exists(tool_path+"/bin/gips_client")):
			print "tool_path: %s not exist" % (tool_path)
			exit(1)
		self.tool_path = tool_path
		self.builder_path = os.getcwd()

	def run(self):
		os.chdir(self.tool_path)
		ret = self.run_gips()
		if ret:
			common.logger.fatal("ThumbnailOperator run_gips error, ret_code:%d, exit" % (ret))
			return ret 

		ret = self.parse_tn()
		if ret:
			common.logger.fatal("ThumbnailOperator run_gips error, ret_code:%d, exit" % (ret))
			return ret 

		os.chdir(self.builder_path)
		return 0

	def run_gips(self):

		common.logger.info("run_gips start")
		os.system("rm -rf ./data/* & ./bin/gips_client ")
		common.logger.info("run_gips over")

	def parse_tn(self):
		if not os.path.exists("./out/success.txt"):
			common.logger.fatal("not found out/result in parse_tn")
			return -1
		file_object = codecs.open("./out/success.txt", 'r', 'utf8')
		try:
		    while True:
				line = file_object.readline()
				if not line:
					break
				(url, tn) = GipsResulsParser.parse(line)
				if url != None and tn != None:
					print 'parse succ, url:%s, tn:%s' % (url, tn)
					self.tn_dict[url] = tn 
				else:
					common.logger.warn('line:%s parse error, url:%s, tn:%s' % (line, url, tn))

		except Exception as e:
			print e.message
			common.logger.error("parse_tn error:%s" % (e.message))
			return -1
		finally:
			file_object.close( )
		return 0


class TnHandler:
	@staticmethod
	def handle(results, tool_path):
		raw_urls = []
		for (key, item) in results.items():
			raw_urls.append(item.picture)
			for link in item.links:
				raw_urls.append(link.img_url_screenshot)

		fd = codecs.open(tool_path + "/conf/url.txt", 'w', 'utf8')
		for url in raw_urls:
			fd.write(url + " 1\r\n")#crop type 1
		fd.close()

		tn_operator = ThumbnailOperator(tool_path)
		ret = tn_operator.run()
		if ret != 0:
			common.logger.fatal("TnHandler handle tool_path:%s, urls num:%d error" % (tool_path, len(raw_urls)))
			return -1

		for (key, item) in results.items():
			if item.picture in tn_operator.tn_dict.keys():
				item.picture = tn_operator.tn_dict[item.picture]
			else:
				item.ignore = True

			for link in item.links:
				if link.img_url_screenshot in tn_operator.tn_dict.keys():
					link.img_url_screenshot = tn_operator.tn_dict[link.img_url_screenshot]
				else:
					item.ignore = True
		return 0


if __name__ == '__main__':
	print "run main"

