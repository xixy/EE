#coding=utf-8
import os

def getFilePath(folder_path, keyword):
	'''
	提取所有的符合某个条件的文件
	'''
	file_paths = []

	files = os.listdir(folder_path)
	for single_file in files:
		# 如果符合条件
		if keyword in single_file:
			file_paths.append(folder_path + single_file)

	return file_paths

if __name__ == '__main__':
	folder_path = '../../data/ace_2005_td_v7/data/Chinese/bn/adj'
	print getFilePath(folder_path, 'sgm')
