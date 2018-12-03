#coding=utf-8
class event(object):
	"""对event进行描述的类"""
	def __init__(self,):
		self.event_mention = event_mention # mention 例如'攻击'
		self.event_mention_offset = event_mention_offset # 在整段中的offset
		self.event_mention_sentence_id = event_mention_sentence_id # 在整段中的第几句 从0开始
		self.doc_id = doc_id # 文本ID CBS20001006.1000.0074
		self.event_id = event_id # 事件id CBS20001006.1000.0074-EV1-1
		self.event_type = event_type
		


