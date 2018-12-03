1. 从sgm文件中提取段落
    ext = extractor()
    # 从sgm文件中提取段落
    ext.extract_param()
2. 对段落进行分句
	String targetFilePath = "/Users/apple/Documents/开题报告/开题报告/代码/event_extraction/EventExtractionProject/preprocess/extractor/sentences.txt";
	String file_path = "/Users/apple/Documents/开题报告/开题报告/代码/event_extraction/EventExtractionProject/preprocess/extractor/param_as_sentence.dat”;
	splitFileSentence(file_path, targetFilePath);
3. 对分句进行标注，得到BIO标注结果
    ext = extractor()
    ext.create_sequence_tag()
4. 对标注结果在进行分句	
	String train_tagged_file_path = "/Users/apple/Documents/开题报告/开题报告/代码/event_extraction/EventExtractionProject/preprocess/extractor/train_data.txt";
	String train_tagged_file_one_sentence_path = "/Users/apple/Documents/开题报告/开题报告/代码/event_extraction/EventExtractionProject/preprocess/extractor/train.data.one.sentence.txt";
	String test_tagged_file_path = "/Users/apple/Documents/开题报告/开题报告/代码/event_extraction/EventExtractionProject/preprocess/extractor/test_data.txt";
	String test_tagged_file_one_sentence_path = "/Users/apple/Documents/开题报告/开题报告/代码/event_extraction/EventExtractionProject/preprocess/extractor/test.data.one.sentence.txt”;
	splitTaggedText(train_tagged_file_path,train_tagged_file_one_sentence_path );
	splitTaggedText(test_tagged_file_path,test_tagged_file_one_sentence_path );

最终得到的标注结果为训练集和测试集合，分别是
1. 以句子为单位
train.data.one.sentence.txt
test.data.one.sentence.txt
2. 以完整的句子为单位
train_data.txt
test_data.txt
都存储在data文件下用于保存