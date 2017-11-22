import json, csv, bson
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
			#break
	#print(names_dict)
	#print(files_table)
	print(len(files_table))
generate_dicts()

with open('name.csv','w') as fle:
	writer = csv.writer(fle)
	writer.writerows([files_table])

with open('name.csv','r') as fle:
	reader = csv.reader(fle)
	for row in reader:
		files_table2 = row

print("files_table is ok: "+str(files_table==files_table2))

for tp in ['Not Shortened','Shortened']:
	print('\n'+tp + " Version:")

	with open('index'+tp+'.json', 'w') as fp:
	    json.dump(names_dict, fp)

	with open('index'+tp+'.json', 'r') as fp:
	    names_dict2=json.load(fp)

	print("\nnames_dict json is ok: "+str(names_dict==names_dict2))
	print("Size in json: "+ str(os.stat('index'+tp+'.json').st_size)+" bytes")

	with open('index'+tp+'.bson', 'wb') as fp:
	   fp.write(bson.dumps(names_dict))

	with open('index'+tp+'.bson', 'rb') as fp:
	    names_dict2=bson.loads(fp.read())

	print("\nnames_dict bson is ok: "+str(names_dict==names_dict2))
	print("Size in bson: "+ str(os.stat('index'+tp+'.bson').st_size)+" bytes")

	#simple compressed string
	dummystring=''
	for k in names_dict:
		dummystring=dummystring+"|"+k+":"
		for x in names_dict[k]:
			dummystring=dummystring+str(x)+","

	with open('index'+tp+'.scs1', 'w') as fp:
	   fp.write(dummystring)

	names_dict2={}
	with open('index'+tp+'.scs1', 'r') as fp:
		dummystring2=fp.read()
		stt=1
		k=''
		num=0
		for c in dummystring2:
			if stt==0:
				if c==':':
					stt=1
					names_dict2[k]=[]
					num=0
				else:
					k=k+c
			elif stt==1:
				if c=='|':
					k=''
					stt=0
				elif c>='0' and c<='9':
					num=num*10+int(c)-int('0')
				elif c==',':
					names_dict2[k].append(num)
					num=0
				else:
					k=''+c
					stt=0

	print("\nnames_dict scs1 is ok: "+str(names_dict==names_dict2))
	print("Size in scs1: "+ str(os.stat('index'+tp+'.scs1').st_size)+" bytes")

	for k in names_dict:
		for i in range(len(names_dict[k])-1,0,-1):
			names_dict[k][i]-=names_dict[k][i-1]

print("\nscs1: Simple compressed string with : and , acting as separators\n(trying new ways to compress it)")
