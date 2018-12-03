# coding=utf-8

from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP(r'/Users/apple/Downloads/stanford-corenlp-full-2018-02-27/',quiet=False, port=9001,  lang='zh')

sentence = '清华大学位于北京。'
print nlp.word_tokenize(sentence)
print nlp.pos_tag(sentence)
print nlp.ner(sentence)
print nlp.parse(sentence)
print nlp.dependency_parse(sentence)