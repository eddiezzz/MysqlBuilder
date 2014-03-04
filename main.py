#coding: utf8

from db_operator import *
from job import *
import common

class JobFactory:
	@staticmethod
	def create(language):
		if language == 'th':
			return ThJob()
		if language == 'br':
			return BrJob()
		if language == 'ar':
			return ArJob()
		return None


def usage(name):
	print '''
#Brief: %s is used for getting specific infos from shitu server
#Author: zhengchangshuai@baidu.com

#usage: python %s cfg_file 
	''' % (name, name)

if __name__ == '__main__':

	filename = 'database.cfg'
	conf = MyConf(filename)
	if 0 != conf.parse():
		print "MyConf.parse error from file:%s" % (filename)
		exit(1)

	common.init_log(conf.log_file, conf.log_level)

	job = JobFactory.create(conf.language)
	if not job:
		common.logger.error("job create failed for language:%s" % (conf.language))
		exit(1)
	common.logger.info("job create success for language:%s" % (conf.language))

	if job.init(conf) != 0:
		common.logger.warn("job runner init failed")
		exit(1)
	common.logger.info("job runner init success")

	ret = job.run()
	common.logger.info("job runner run over, ret:%d" % (ret))

	exit(0)
