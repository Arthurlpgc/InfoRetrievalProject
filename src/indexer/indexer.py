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

def bitstr(k):
	if k==0:
		return str(chr(0))
	st=''
	acbit=0
	while k>0:
		st=str(chr(int(k%128)+acbit))+st
		acbit=128
		k=k//128
	return st

def add_st(st,barray,idx):
	for c in st:
		if idx==0:
			barray.append(0)
		barray[-1]|=(int(c)<<idx)
		idx=((idx+1)&7)
	return (barray,idx)

def get_st(barray,idx,sze):
	st=0
	for i in range(sze):
		st=(st<<1)+(1&(barray[0]>>idx))
		if idx==7:
			barray=barray[1:]
		idx=((idx+1)&7)
	return (barray,idx,st)

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

	dummystring=''
	for k in names_dict:
		dummystring=dummystring+k+":"
		for x in range(len(names_dict[k])):
			if(x!=0):
				dummystring=dummystring+","
			dummystring=dummystring+bitstr(names_dict[k][x])
		dummystring=dummystring+"|"

	with open('index'+tp+'.scs2', 'wb') as fp:
	   fp.write(dummystring.encode('utf-8'))

	names_dict2={}
	with open('index'+tp+'.scs2', 'rb') as fp:
		dummystring2=fp.read().decode('utf-8')
		stt=0
		k=''
		num=0
		for c in dummystring2:
			if stt==0:
				if c==':':
					stt=2
					names_dict2[k]=[]
					num=0
				else:
					k=k+c
			elif stt==1:
				if c=='|':
					k=''
					stt=0
					num=0
				elif c==',':
					num=0
					stt=2
			else:
				stt=1+(ord(c)//128)
				num=(num<<7)+(ord(c)&127)
				if stt==1:
					names_dict2[k].append(num)

	for k in names_dict.keys():
		if names_dict[k] != names_dict2[k]:
			print(k)
			print(names_dict[k])
			print(names_dict2[k])
			break
	print("\nnames_dict scs2 is ok: "+str(names_dict==names_dict2))
	print("Size in scs2: "+ str(os.stat('index'+tp+'.scs2').st_size)+" bytes")

	charset=set()
	for k in names_dict:
		for c in k:
			charset.add(c)
	charset=list(charset)
	pot=2**(len(charset).bit_length())

	byte_array=[]
	idx=0
	for k in names_dict:
		(byte_array,idx)=add_st('01',byte_array,idx)
		for c in k:
			Ch="{0:b}".format(charset.index(c))
			while len(Ch)<6:
				Ch="0"+Ch
			(byte_array,idx)=add_st(Ch,byte_array,idx)
		Ch="{0:b}".format(len(charset))
		while len(Ch)<6:
			Ch="0"+Ch
		(byte_array,idx)=add_st(Ch,byte_array,idx)
		for x in names_dict[k]:
			st=''
			saux="11"
			#print('lllll')
			#print(x)
			if(x==0):
				st='10000000'
			while x>0:
				stemp="{0:b}".format(x&63)
				while len(stemp)<6:
					stemp="0"+stemp
				if(x<64):
					saux='10'
				st=st+saux+stemp
				x=x//64
			#print(st)
			(byte_array,idx)=add_st(st,byte_array,idx)
	(byte_array,idx)=add_st('00',byte_array,idx)

	with open('index'+tp+'.scb', 'wb') as fp:
	   fp.write(bytearray(byte_array))

	names_dict2={}

	stt=-1
	idx=0
	k=''
	mul=1
	with open('index'+tp+'.scb', 'rb') as fp:
		byte_array2=fp.read()
		while True:
			if stt==-1:
				(byte_array2,idx,stt)=get_st(byte_array2,idx,2)
			elif stt==1 or stt==4:
				(byte_array2,idx,st)=get_st(byte_array2,idx,6)
				if st<len(charset):
					if stt==1:
						k=''
					k=k+charset[st]
					stt=4
				else:
					names_dict2[k]=[]
					stt=-1
					num=0
			elif stt==3:
				(byte_array2,idx,st)=get_st(byte_array2,idx,6)
				num=num+int(st)*mul
				mul=mul*64
				stt=-1
			elif stt==2:
				(byte_array2,idx,st)=get_st(byte_array2,idx,6)
				num=num+int(st)*mul
				names_dict2[k].append(num)
				stt=-1
				mul=1
				num=0
			else:
				break

	print("\nnames_dict scb is ok: "+str(names_dict==names_dict2))
	print("Size in scb: "+ str(os.stat('index'+tp+'.scb').st_size)+" bytes")

	for k in names_dict:
		for i in range(len(names_dict[k])-1,0,-1):
			names_dict[k][i]-=names_dict[k][i-1]

print("\nscs1: Simple compressed string with : and , acting as separators\n(trying new ways to compress it)")
print("\nscs2: scs1 + base 128 varInt")
