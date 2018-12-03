#coding=utf-8
import xml.etree.cElementTree as ET
import os
from pathutil import *
import re
from configure import *
from str_util import *
import HTMLParser
from split_data import *



class extractor(object):
	"""从ace原始文件中提取信息"""

	def __init__(self, ace_path = '../../data/ace_2005_td_v7'):
		self.ace_path = ace_path
		self.middle_file_path = './middle_result.dat'
		self.param_as_sentence_path = './param_as_sentence.dat'
		self.sentences_path = './sentences.txt'
		self.sequence_tag_path = './sentences.tagged.txt'


		self.train_data_path = './train_data.txt'
		self.test_data_path = './test_data.txt'
		self.dev_data_path = './dev_data.txt'

		# train、dev、test数据集所包含的ace文件列表
		self.train_ace_file_list = getFilesForDataSets('../../data/ace_data/train/train.word.dat')
		self.dev_ace_file_list = getFilesForDataSets('../../data/ace_data/dev/dev.word.dat')
		self.test_ace_file_list = getFilesForDataSets('../../data/ace_data/test/test.word.dat')

		# 输出文件
		self.train_output_file = open(self.train_data_path,'w')
		self.dev_output_file = open(self.dev_data_path,'w')
		self.test_output_file = open(self.test_data_path,'w')

	def delete_blank(self, string):
		'''
		去掉所有的空格
		'''
		if type(string) is str:
			return string.replace('\n','').replace(' ','').replace('　', '')
		return string.replace('\n','').replace(' ','').encode('utf-8').replace('　', '')

	def parse_apf_xml(self, file_path='../../data/ace_2005_td_v7/data/Chinese/bn/adj/CBS20001006.1000.0074.apf.xml'):
		'''
		从***.apf.xml文件中提取事件
		包括:anchor,extent,ldc_scope,type
		'''
		events = []

		tree = ET.ElementTree(file=file_path)
		root = tree.getroot()
		for elem in tree.iter(tag = 'event'):
			e_type = elem.attrib[event_type]
			e_sub_type = elem.attrib[event_sub_type]
			
			for child in elem:
				if 'event_mention' in child.tag:
					event = {}
					event[event_type] = e_type
					event[event_sub_type] = e_sub_type
					event[arguments] = []
					for item in child:
						# 提取anchor
						if anchor in item.tag:
							event[anchor] = self.delete_blank(item[0].text)
							event[anchor_offset] = [int(item[0].attrib[offset_start]),int(item[0].attrib[offset_end])]
						# 提取extent
						if extent in item.tag:
							event[extent] = self.delete_blank(item[0].text)
						# 提取ldc_scope
						if ldc_scope in item.tag:	
							event[ldc_scope] = self.delete_blank(item[0].text)
							event[ldc_scope_offset] = [int(item[0].attrib[offset_start]),int(item[0].attrib[offset_end])]
						# 提取event_mention_argument
						if event_mention_argument in item.tag:
							argument = {}
							argument[role] = item.attrib[role].encode('utf-8')
							argument[event_mention_argument] = self.delete_blank(item[0][0].text)
							event[arguments].append(argument)

					events.append(event)
		return events

	def extract_param(self):
		'''
		从sgm文件中提取段落文本, 每段用空格隔开，然后拼接成一行，去掉空格和URL
		'''

		# 首先从sgm文件中提取文本，存入到middle_result.dat文件中

		middle_file = open(self.middle_file_path, 'w')
		count = 0

		# 先处理 bn 部分
		folder = self.ace_path + '/' + 'data/Chinese/bn/adj/'
		sgm_files = getFilePath(folder, 'sgm')

		for sgm_file in sgm_files:
			count += 1
			param = ''
			middle_file.write(sgm_file)
			tree = ET.ElementTree(file = sgm_file)
			root = tree.getroot()
			for elem in root[3]:
				for turn in elem:
					param += turn.text
			param = param.replace(' ', '')
			# param =
			middle_file.write(param.encode('utf-8'))

		# 处理nw部分
		folder = self.ace_path + '/' + 'data/Chinese/nw/adj/'
		sgm_files = getFilePath(folder, 'sgm')

		for sgm_file in sgm_files:
			count += 1
			param = ''
			middle_file.write(sgm_file)
			tree = ET.ElementTree(file = sgm_file)
			root = tree.getroot()
			text = root[3][1].text

			param = text.replace(' ', '')
			middle_file.write(param.encode('utf-8'))

		# 处理wl部分, 需要用文本的方法进行处理，没法用xml解析
		folder = self.ace_path + '/' + 'data/Chinese/wl/adj/'
		sgm_files = getFilePath(folder, 'sgm')
		for sgm_file in sgm_files:
			count += 1
			middle_file.write(sgm_file + '\n')
			param = ''
			InText = False
			for line in open(sgm_file):
				if '</POST>' in line:
					InText = False
				if InText:
					param += line
				if '<POSTDATE>' in line:
					InText = True
			param.replace(' ', '')
			middle_file.write(param)

		middle_file.close()

		# 从middle_result.dat中读取刚才生成的中间结果，拼接成一个段落一句
		data = {}
		param = ''
		current_file = None

		for line in open(self.middle_file_path, 'r'):
			line = line.strip()

			# 如果是文件列表行
			if '../../data' in line:
				data[line] = []
				# output_file.write(line + '\n')

				# 如果是前面的结束，把这段加进去
				if param != '':
					data[current_file].append(param)
					param = ''
				current_file = line
				continue

			# 如果是空行，一段结束, 就把这个段落加进去
			if len(line) < 1:
				if param != '':
					# 去掉空格
					param.replace(' ','')
					param.replace('\n', '')
					data[current_file].append(param)
					param = ''
			# 否则就把这行并起来
			else:
				# 如果是URL行，就扔掉
				if not self.is_URL(line):
					param += line

		# 结果写入文件
		output_file = open(self.param_as_sentence_path,'w')
		for file_path in data:
			output_file.write(file_path + '\n')
			for param in data[file_path]:
				output_file.write(param + '\n') 
		output_file.close()



	def is_URL(self, text):
		'''
		判断是否URL
		'''
		if 'http://' in text and '.html' in text:
			return True
		return False

	def printlist(self, sentences_with_events):
		print '---------------打印-----------'
		for scope, event in sentences_with_events:
			print scope
			for item in event:
				print item[ldc_scope],item[anchor]

	def find_indexes(self, indexs, begin, article, event):
		'''
		查找该事件对应的几个句子，返回首尾的index
		Args:
			indexs:[[0,10],[11,16]...]
			begin: 表示在文章中查找的起始位置
			article:表示句子

		Return:
			start_idx:
			end_idx
			start:表示ldc_scope在段落中的起始位置
			end: 表示ldc_scope在段落中的结束位置
		'''
		# 先找到范围
		start = article.index(event[ldc_scope],begin)
		end = start + len(event[ldc_scope]) - 1
		start_idx = None # 文章中开始的句子id
		end_idx = None # 文章中结束的句子id
		
		for idx in indexs:
			# 先判断起始位置
			if start_idx == None and idx[0] <= start:
				# 如果都小于开头，那就不在当前句子
				if idx[1] < start:
					continue
				# 如果结尾大于开头，那开始部分就是当前句子
				else:
					start_idx = indexs.index(idx)
			# 然后判断终止位置
			if idx[1] >= end:
				end_idx = indexs.index(idx)
				break
		return start, end, start_idx, end_idx

	def map_events_articles(self, events, lines, article, file_path):
		'''
		将events和文章对应起来
		Args:
			events:[event]
			lines: [line]每行是一个分出来的句子
			article: 一篇文章拼接起来的string
			file_path: 该文章所在的路径
		'''

		# 首先统计句子的边界信息
		sentences_with_events = []
		count = 0
		indexs = [] # 每个句子的起始index和结尾index
		for sentence in lines:
			indexs.append([count, count + len(sentence) - 1])
			count += len(sentence)


		# 然后针对事件信息来进行对齐
		for event in events:

			# 如果ldc_scope不在句子中，那么就报错
			if event[ldc_scope] not in article or event[extent] not in article:
				raise Exception('出现了找不到的文本')
			# 现在进行处理
			begin_idx = 0
			find_right_index = False

			while find_right_index == False:
				start, end, start_idx, end_idx = self.find_indexes(indexs, begin_idx, article, event) # 找到indexes

				# 将事件对应的句子进行记录
				scopes = [i for i in range(start_idx, end_idx + 1)]

				# 将scope和event进行存储
				index = 0
				for item in sentences_with_events:
					# 如果该scopes已经存在，那么就放进去
					if item[0] == scopes:
						break
					index += 1

				# 如果scopes已经存在
				if index < len(sentences_with_events):
					same_exist = False
					# 如果不相同，就直接extend

					anchor_idx = 0
					for former_event in sentences_with_events[index][1]:
						# 如果事件基本相同
						if former_event[anchor] == event[anchor] and former_event[ldc_scope] == event[ldc_scope] \
						and former_event[ldc_scope_offset] != event[ldc_scope_offset]:

							# print former_event[anchor],former_event[ldc_scope]
							# print event[anchor], event[ldc_scope]
							same_exist = True
							break
					# 如果没有相同的
					if same_exist == False:
						sentences_with_events[index][1].extend([event])
						find_right_index = True
					# 如果有相同的，就需要继续找
					else:
						begin_idx = end

				# 如果scope不存在，就直接新建
				else:
					sentences_with_events.append([scopes, [event]])
					find_right_index = True

			# if len(scopes) < 2:
			# 	continue
			# print 'ldc_scope------------------------------111111111111-------'
			# print event[ldc_scope]
			
			# print 'mapped sentences-------------------------000000000000------'
			# for scope in scopes:
			# 	print '[' + str(scope)+ ']' + lines[scope]


		# 处理事件可能的重叠
		scopes_with_events = {}
		events_loaded = [] # 已经被归并的事件
		flag = True # 如果一次循环没有发生变化，那就是合并结束了
		# overlapped = True 

		# 只要发生一次合并，就循环
		while flag == True:
			# self.printlist(sentences_with_events)

			flag = False
			scopes_with_events = []
			events_loaded = []

			i = 0
			while i < len(sentences_with_events):
				overlapped = False
				scope1, events1 = sentences_with_events[i]
				if events1 in events_loaded:
					i += 1
					continue

				j = i + 1
				while j < len(sentences_with_events):
					scope2, events2 = sentences_with_events[j]
					if events2 in events_loaded:
						j += 1
						continue
					# 如果有重叠
					if intersect(scope1, scope2) != []:
						# print scope1, scope2
						flag = True # 发生了重叠
						new_scope = union(scope1, scope2)
						new_events = events1 + events2
						scopes_with_events.append([new_scope, new_events])
						events_loaded.append(events1)
						events_loaded.append(events2)

						overlapped = True
					j += 1

				# 如果没有重叠
				if overlapped == False:
					scopes_with_events.append([scope1, events1])
					events_loaded.append(events1)
				i += 1

			# 更新
			sentences_with_events = scopes_with_events

		# self.printlist(sentences_with_events)

		# 对结果进行输出
		return sentences_with_events




	def write_sequence_tag(self, sentences_with_events, output_file, lines):
		'''
		对结果进行输出
		'''
		# 先输出有事件的句子，并且统计有事件的句子
		
		# output_file.write(str(len(lines)))
		if len(lines) < 1:
			raise Exception('文章为空')
		scopes_with_events = []# 包含了事件的句子id
		for scopes, events in sentences_with_events:

			scopes_with_events.extend(scopes)# 对有事件的句子统计
			line = ''.join([lines[i] for i in scopes])
			line = line.decode('utf-8')
			anchor_indexs = []
			# 找到anchor的index
			for event in events:
				# 先找ldc_scope的index，然后用anchor的offset计算即可

				# 先找ldc_scope的index，这是唯一的
				ldc_scope_index = line.index(event[ldc_scope].decode('utf-8'))
				# 然后找anchor的index，但是可能offset信息不准，有空格和换行的存在，所以只能通过这个来算一个大概范围
				anchor_index_begin = ldc_scope_index + event[anchor_offset][0] - event[ldc_scope_offset][0] - buffer_scope
				if anchor_index_begin < 0:
					anchor_index_begin = 0

				try:
					# 然后从这个位置开始找第一个，应该是对的？
					anchor_index = line.index(event[anchor].decode('utf-8'),anchor_index_begin)
				except Exception, e:
					print line.encode('utf-8')
					print 'anchor:' + event[anchor]
					print anchor_index_begin
					print '截断句子:' + line[anchor_index_begin:].encode('utf-8')
					print event[ldc_scope]
					# print event[anchor_offset]
					raise Exception('找不到对应的index')

				# print '------------------------------------'
				# print 'anchor:' + event[anchor]
				# # print anchor_index
				# # print anchor_index_begin
				# print '句子:' + line.encode('utf-8')
				# print '有效句子:' + line[anchor_index:].encode('utf-8')
				# print 'ldc_scope:' + event[ldc_scope]

				anchor_indexs.append([anchor_index, event])

			# 对该socpes进行输出
			tagged_scope = []
			for char in line:
				tagged_scope.append([char, 'O'])
			for anchor_index, event in anchor_indexs:
				# 计算BIO
				tagged_scope[anchor_index][1] = 'B-' + event[event_sub_type]
				for i in range(anchor_index + 1, anchor_index + len(event[anchor].decode('utf-8'))):
					tagged_scope[i][1] = 'I-' + event[event_sub_type]

			# 进行输出
			for char, tag in tagged_scope:
				output_file.write(char.encode('utf-8') + ' '+ tag + '\n')

			output_file.write('\n')



		# 然后输出没有事件的句子
		if output_file == self.dev_output_file or output_file  == self.test_output_file:
			if remove_empty_instance:
				return
		for i in range(len(lines)):
			if i not in scopes_with_events:
				for char in lines[i].decode('utf-8'):
					output_file.write(char.encode('utf-8') + ' O' + '\n')
				output_file.write('\n')


	def get_output_file(self, line):
		'''
		根据文件列表名来判断应该输出到train、dev、test哪个文件
		Args:
			line:../../data/ace_2005_td_v7/data/Chinese/bn/adj/CTS20001218.1300.0965.sgm
		'''
		name = line[-21:]
		if name in self.train_ace_file_list:
			return self.train_output_file
		elif name in self.test_ace_file_list:
			return self.test_output_file
		else:
			return self.train_output_file

	def create_sequence_tag(self):
		'''
		根据分句之后的结果，将句子进行标记，以字为单位
		'''
		html_parser = HTMLParser.HTMLParser()
		# output_file = open(self.sequence_tag_path,'w')
		events = None # 从apf文件中提取的事件信息
		file_path = None # 表示事件的文件
		lines = [] # 表示句子的集合
		article = '' # 表示文章的str

		# 对结果进行统计
		events_number = 0
		article_number = 0
		lines_number = 0


		with open(self.sentences_path) as f:
			for line in f:
				line = line.strip()
				# 如果是文件列表行
				if '../data' in line:
					# 如果上一篇文章处理完毕，接下来进行事件的对应
					if len(lines) > 1:
						output_file = self.get_output_file(file_path)
						sentences_with_events = self.map_events_articles(events, lines, article, file_path)
						self.write_sequence_tag(sentences_with_events, output_file, lines)


					article = ''
					lines = []
					# 提取这个文件对应的apf文件中的事件
					file_path = line[:-4]
					events = self.parse_apf_xml(line[:-4]+'.apf.xml')
					events_number += len(events)
					article_number += 1

				# 如果不是的话
				else:
					line = line.decode('utf-8')
					line = html_parser.unescape(line)
					line = line.encode('utf-8')
					line = self.delete_blank(line)

					lines.append(line)
					article += line
					lines_number += 1

		self.train_output_file.close()
		self.dev_output_file.close()
		self.test_output_file.close()
		# 对统计结果进行输出
		print '解析结束，总共解析到' + str(events_number) + '个事件'
		print '总共有' + str(article_number) + '篇文章'
		print '总共有' + str(lines_number) + '句话'
		print 'train set包括ACE中' + str(len(self.train_ace_file_list)) + '个文件'
		print 'dev set包括ACE中' + str(len(self.dev_ace_file_list)) + '个文件'
		print 'test set包括ACE中' + str(len(self.test_ace_file_list)) + '个文件'
					

if __name__ == '__main__':
	ext = extractor()
	# 从sgm文件中提取段落
	# ext.extract_param()
	# print ext.parse_apf_xml()
	ext.create_sequence_tag()





		