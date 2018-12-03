#coding=utf-8
import re

def split_sentences(sentence):
	'''
	对句子进行拆分，因为ldc_scope或者extent可能是两个句子
	'''
	sentences = re.split('(。|！|\!|\.|？|\?)',sentence)
	return sentences

def intersect(a, b):
	'''
	求两个list的交集
	'''
	# print a
	# print b
	return list(set(a).intersection(set(b)))

def union(a, b):
	'''
	求两个list的并集
	'''
	# print a, b
	# print list(set(a).union(set(b)))
	return list(set(a).union(set(b)))
    
    
if __name__ == "__main__":
    a = '我的弟妇为人温柔、善良且娴淑。结婚12年'
    b = '结婚12年来，她凡事都尊重我弟弟的意见，绝对是个好太太、好妈妈。”'
    for sentence in  split_sentences(a):
    	print sentence