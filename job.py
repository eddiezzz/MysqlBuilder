#coding: utf8

from job_interface import *
import common
from xml.etree import ElementTree as ET
import codecs
import random
import copy
import pdb
import thumbnail

class VideoLinkFormat:
	link_fields = ['link_priority', 'link_title', 'link_picture', 'link_duration', 'link_source_url', 'link_subtitle']
	def __init__(self):
		self.priority = 0
		self.custom_title = ''
		self.img_url_screenshot = ''
		self.duration = 0
		self.source_url = ''
		self.subtitle = 0
	
	def valid(self):
		if self.custom_title == None or len(self.custom_title) == 0:
			self.custom_title = 'NULL'
		if self.img_url_screenshot == None or len(self.img_url_screenshot) == 0:
			self.img_url_screenshot = 'NULL'
		if self.source_url == None or len(self.source_url) == 0:
			self.source_url= 'NULL'
		self.subtitle = 0 if self.subtitle!=1 else 1

class ResultFormat():
	sep = '\t'
	fields = ['title', 'norm_title', 'show_time', 'actor', 'director', 'tag', 'location', 'intro', 'picture']
	def __init__(self):
		sep = '\t'
		self.id = 0
		self.title = ''
		self.norm_title = ''
		self.show_time = 0
		self.actor = ''
		self.director = ''
		self.tag = ''
		self.location = ''
		self.intro = ''
		self.picture = ''
		self.duration = 0
		self.links = []
		self.ignore = False

	def valid(self):
		if self.ignore == True:
			return False
		if self.title == None or len(self.title) == 0:
			self.title = 'NULL'
		if self.norm_title == None or len(self.norm_title) == 0:
			self.norm_title = 'NULL'
		if self.actor == None or len(self.actor) == 0:
			self.actor = 'NULL'
		if self.director == None or len(self.director) == 0:
			self.director = 'NULL'
		if self.tag == None or len(self.tag) == 0:
			self.tag = 'NULL'
		if self.location == None or len(self.location) == 0:
			self.location = 'NULL'
		if self.intro == None or len(self.intro) == 0:
			self.intro = 'NULL'
		if self.picture == None or len(self.picture) == 0:
			self.picture = 'NULL'

		for link in self.links:
			link.valid()

		#if type(self.show_time) != type(1) and type(self.show_time) != type(1.1) and type(self.show_time) != type(1L):
		if type(self.show_time) != type('str'):
			self.show_time = common.timestamp_to_string(self.show_time)

		return True


	@staticmethod
	def excel_fields():
		return 'key' + ResultFormat.sep + ResultFormat.sep.join(ResultFormat.fields + VideoLinkFormat.link_fields)

	def excel_create(self, key):
		if self.valid() == False:
			return None

		parent = ""
		parent += "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (
				key, ResultFormat.sep,  \
				self.title.decode('utf8', 'ignore'), ResultFormat.sep,  \
				self.norm_title.decode('utf8', 'ignore'), ResultFormat.sep,  \
				self.show_time, ResultFormat.sep, \
				self.actor.decode('utf8', 'ignore'), ResultFormat.sep, \
				self.director.decode('utf8', 'ignore'), ResultFormat.sep, \
				self.tag.decode('utf8', 'ignore'), ResultFormat.sep, \
				self.location.decode('utf8', 'ignore'), ResultFormat.sep, \
				self.intro.decode('utf8', 'ignore'), ResultFormat.sep, \
				self.picture)
		parent += "\n"

		for link in self.links:
			indent_prefix = ResultFormat.sep.join(['-']*len(ResultFormat.fields)) + ResultFormat.sep + '-'
			parent += indent_prefix + ResultFormat.sep
			parent += "%s%s%s%s%s%s%s%s%s%s%d" % (link.priority, ResultFormat.sep, \
					link.custom_title.decode('utf8', 'ignore'), ResultFormat.sep, \
					link.img_url_screenshot, ResultFormat.sep, \
					link.duration, ResultFormat.sep, \
					link.source_url, ResultFormat.sep, \
					link.subtitle)
			parent += "\n"
		return parent


	def xml_create(self, parent, i, key):
		if self.valid() == False:
			return None
		item = ET.SubElement(parent, 'video_description', index=('%s' %i))
		keyItem = ET.SubElement(item, 'key')
		keyItem.text = key#.decode('utf8', 'ignore')
		title = ET.SubElement(item, 'title')
		title.text = self.title.decode('utf8', 'ignore')
		norm_title = ET.SubElement(item, 'norm_title')
		norm_title.text = self.norm_title.decode('utf8', 'ignore')

		show_time = ET.SubElement(item, 'show_time')
		show_time.text = '%s' % (self.show_time)
		actor = ET.SubElement(item, 'actor')
		actor.text = self.actor.decode('utf8', 'ignore')
		director = ET.SubElement(item, 'director')
		director.text = self.director.decode('utf8', 'ignore')
		tag = ET.SubElement(item, 'tag')
		tag.text = self.tag.decode('utf8', 'ignore')
		location = ET.SubElement(item, 'location')
		location.text = self.location.decode('utf8', 'ignore')
		intro = ET.SubElement(item, 'intro')
		intro.text = self.intro.decode('utf8', 'ignore')
		picture = ET.SubElement(item, 'picture')
		picture.text = self.picture


		links = ET.SubElement(item, 'links')
		for i in self.links:
			link = ET.SubElement(links, 'link')
			priority = ET.SubElement(link, 'priority')
			priority.text = '%s' % (i.priority)
			custom_title = ET.SubElement(link, 'custom_title')
			custom_title.text = i.custom_title.decode('utf8', 'ignore')
			img_url_screenshot = ET.SubElement(link, 'img_url_screenshot')
			img_url_screenshot.text = i.img_url_screenshot

			duration = ET.SubElement(link, 'duration')
			duration.text = '%s' % (i.duration)

			source_url = ET.SubElement(link, 'source_url')
			source_url.text = i.source_url

			subtitle = ET.SubElement(link, 'subtitle')
			subtitle.text = '%s' % (i.subtitle)
		return True

class XmlCreator():
	def create(self, results, filename):
		root = ET.Element('videos')
		i = 0
		for (key,item) in results.items():
			if None != item.xml_create(root, i, key):
				i += 1

		tree = ET.ElementTree(root)
		tree.write(filename, encoding='utf8')
		
class ExcelCreator():
	def create(self, results, filename):
		root = ResultFormat.excel_fields()
		root += "\n"
		for (key,item) in results.items():
			ret = item.excel_create(key)
			if ret != None:
				root += ret

		fd = codecs.open(filename, 'w', 'utf8')
		fd.write(root)
		fd.close()


class JobCenter:
	@staticmethod
	def video_and_link(job_interface):
		loc_ids = {}
		if job_interface.conf.language == 'br':
			loc_req = 'select id,name from location_name_long_br where is_online = 1;'
			rows, locs = job_interface.db.query(loc_req)
			for i in range(0, rows):
				loc_ids["%s" % locs[i][0]] = locs[i][1]
		
		req_str = ('id', 'title', 'norm_title', 'show_time', 'actor', 'director', 'tag', 'location', 'intro', 'picture', 'duration')
		constrain = ''
		if job_interface.conf.language == 'ar':
			constrain = 'is_online = 1 and catalog = "0" and picture IS NOT NULL'
		else:
			constrain = 'is_online = 1 and catalog = 0 and picture IS NOT NULL'

		if job_interface.conf.task1_result_limit > 0:
			constrain += ' order by rand()'
			constrain += ' limit 0, %d' % (job_interface.conf.task1_result_limit)

		sql = 'select %s from %s where %s;' % (",".join(req_str), job_interface.conf.db_description_table, constrain)
		#print sql
		rows, video_ids = job_interface.db.query(sql)
		results = {}
		for i in range(0, rows):
			item = ResultFormat()
			item.id = video_ids[i][0]
			item.title = None if video_ids[i][1] is None else video_ids[i][1].encode('utf8').strip()
			item.norm_title = None if video_ids[i][2] is None else video_ids[i][2].encode('utf8').strip()
			item.show_time = 0 if video_ids[i][3] is None else video_ids[i][3]
			item.actor = None if video_ids[i][4] is None else video_ids[i][4].strip()
			item.director = None if video_ids[i][5] is None else video_ids[i][5].strip()
			item.tag = None if video_ids[i][6] is None else video_ids[i][6].strip()
			if len(loc_ids) == 0:
				item.location = None if video_ids[i][7] is None else video_ids[i][7].strip()
			else:
				item.location = None if video_ids[i][7] is None else (loc_ids[video_ids[i][7].strip()] if video_ids[i][7].strip() in loc_ids else video_ids[i][7].strip())
			item.intro = None if video_ids[i][8] is None else video_ids[i][8].strip()
			item.picture = None if video_ids[i][9] is None else video_ids[i][9].strip()
			##test gips
			#item.picture = 'http://img0.bdstatic.com/img/image/meinvshoujiao.jpg'

			item.duration = 0 if video_ids[i][10] is None else video_ids[i][10]
			if item.picture is not None and len(item.picture) > 0:
				if item.norm_title is not None and len(item.norm_title) > 0:
					results[item.norm_title] = item #last norm_title win
				if item.title is not None and len(item.title) > 0 and item.title not in results.keys(): #first title win, norm_title always wins title
					results[item.title] = copy.copy(item)
			else:
				print "video title:%s, id:%d picture is none" % (item.title,item.id)
			

		req_str2 = ''
		if job_interface.conf.language == 'ar':
			req_str2 = ['priority','norm_title','img_localid_screenshot','duration','source_url']
		else:
			req_str2 = ['priority','custom_title','img_localid_screenshot','duration','source_url']
		for item in results.values():
			sql = 'select %s from %s where id in ( select link_id from %s where description_id = %d and is_online = 1);' % (",".join(req_str2), job_interface.conf.db_link_table, job_interface.conf.db_relation_table, item.id)
			link_count, links = job_interface.db.query(sql)
			tmp_items = []
			random.seed(item.id)
			for i in range(0, link_count):
				link_item = VideoLinkFormat()
				link_item.priority = 0 if links[i][0] is None else links[i][0]
				link_item.custom_title = None if links[i][1] is None else links[i][1]
				##test gips
				link_item.img_url_screenshot = None if links[i][2] is None else links[i][2].strip()
				#link_item.img_url_screenshot = 'http://imgstatic.baidu.com/img/image/mingxing640.jpg'
				link_item.duration = 0 if links[i][3] is None else links[i][3]
				link_item.source_url = None if links[i][4] is None else links[i][4]

				if link_item.duration <= 0 and item.duration > 0:
					link_item.duration = item.duration*60 - 120 + random.randint(0, 240)
					link_item.duration = 0 if link_item.duration < 0 else link_item.duration
				#if link_item <= 0:
				#	link_item.duration = random.randint(10*60, 120*60)
					
				if link_item.priority == 0:
					link_item.priority = job_interface.conf.site_dict.get_priority(link_item.source_url)
				tmp_items.append(link_item)
			tmp_items = sorted(tmp_items, key=lambda s: s.priority, reverse=True)
			item.links = tmp_items
			print "running for id:%d, title:%s, norm_title:%s, links:%d" % (item.id, item.title, item.norm_title, link_count)
			#common.logger.info("running for id:%d, title:%s, norm_title:%s, links:%d" % (item.id, item.title, item.norm_title, link_count))

		if job_interface.conf.thumbnail_process == 1:
			ret = thumbnail.TnHandler.handle(results, job_interface.conf.tool_path)
			if ret != 0:
				return -1

		if job_interface.conf.task1_excel_output == 1:
			excel_creator = ExcelCreator()
			excel_creator.create(results, job_interface.conf.task1_output_dir + '/' + job_interface.conf.language + '_data.txt')
		if job_interface.conf.task1_xml_output == 1:
			xml_creator = XmlCreator()
			xml_creator.create(results, job_interface.conf.task1_output_dir + '/' + job_interface.conf.language + '_data.xml')
		return 0

	@staticmethod
	def data_statistic(job_interface):
		str_fields = job_interface.conf.task3_str_fields.split(',')
		for field in str_fields:
			sql = 'select count(*) from %s where is_online = 1 and catalog = 0 and %s IS NOT NULL and LENGTH(TRIM(%s)) > 0;' \
				  % (job_interface.conf.db_description_table, field, field)
			rows, res_data = job_interface.db.query(sql)
			if rows <= 0:
				print '%s: error' % (field)
			else:
				print '%s: %d' % (field, res_data[0][0])

		int_fields = job_interface.conf.task3_int_fields.split(',')
		for field in int_fields:
			sql = 'select count(*) from %s where is_online = 1 and catalog = 0 and %s IS NOT NULL and %s > 0;' \
				  % (job_interface.conf.db_description_table, field, field)
			rows, res_data = job_interface.db.query(sql)
			if rows <= 0:
				print '%s: error' % (field)
			else:
				print '%s: %d' % (field, res_data[0][0])
		return 0

class ThJob(JobInterface):
	def run(self):
		if self.conf.task1_is_open == 1:
			JobCenter.video_and_link(self)
		if self.conf.task3_is_open == 1:
			JobCenter.data_statistic(self)
		return 0

		
class BrJob(JobInterface):
	def run(self):
		if self.conf.task1_is_open == 1:
			JobCenter.video_and_link(self)
		if self.conf.task3_is_open == 1:
			JobCenter.data_statistic(self)
		return 0


class ArJob(JobInterface):
	def run(self):
		if self.conf.task1_is_open == 1:
			JobCenter.video_and_link(self)
		if self.conf.task3_is_open == 1:
			JobCenter.data_statistic(self)
		return 0

