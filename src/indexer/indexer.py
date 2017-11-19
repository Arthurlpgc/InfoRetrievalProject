import json
import os
from pprint import pprint
import re
import math

def get_json_data(path):
	dir = os.path.dirname(os.path.realpath('__file__'))
	filename = os.path.join(dir, 'retrieved/objects/' ,path + '.json')
	json_data=open(filename).read()
	data = json.loads(json_data)
	ret = {'file': path.split('/')[-1]}
	stt=re.sub("[^\w]", " ",  data['statement']).split()
	stt=list(map(lambda x:x.lower(),stt))
	sttf=[]
	for wordy in stt:
		if wordy not in sttf:
			sttf.append(wordy)
	ret['statement']=sttf
	tt=re.sub("[^\w]", " ",  data['title']).split()
	tt=list(map(lambda x:x.lower(),tt))
	ttf=[]
	for wordy in tt:
		if wordy not in ttf:
			ttf.append(wordy)
	ret['title']=ttf
	tme=data['time-limit']
	if tme%200:
		tme=tme+200-tme%200
	ret['time']=tme
	if data['memory-limit'] != -1:
		ret['memorylog']=int(math.log(data['memory-limit'],2))
	else:
		ret['memorylog']=-1
	return ret

files_table = []
names_dict = {}

def put_word(word, idx):
	if word not in names_dict.keys():
		names_dict[word]=[]
	names_dict[word].append(idx)

def insert_entry(hsh):
	files_table.append(hsh['file'])
	idx = len(files_table)-1
	for word in hsh['statement']:
		put_word(word+".statement",idx)
	for word in hsh['title']:
		put_word(word+".title",idx)
	put_word(str(hsh['time'])+".time",idx)
	put_word(str(hsh['memorylog'])+".mem",idx)

def generate_dicts():
	dir = os.path.dirname(os.path.realpath('__file__'))
	filename = os.path.join(dir, 'retrieved/objects/')
	for path in os.listdir(filename):
		if 'json' in path:
			data = get_json_data(path[:-5])
			insert_entry(data)
	#print(names_dict)
	#print(files_table)
	print(len(files_table))
generate_dicts()
