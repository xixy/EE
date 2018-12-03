#coding=utf-8

def getFilesForDataSets(filename):
	'''
	从NPN模型的数据中获取到trian、dev、test数据的对应文件
	'''
	files = set() # 该数据集对应的文件id
	with open(filename) as f:
		for line in f:
			line = line.strip()
			line = line.split('	')
			files.add(line[0])
	return files

if __name__ == '__main__':
	print len(getFilesForDataSets('../../data/ace_data/dev/dev.word.dat'))
	print len(getFilesForDataSets('../../data/ace_data/train/train.word.dat'))
	print len(getFilesForDataSets('../../data/ace_data/test/test.word.dat'))


