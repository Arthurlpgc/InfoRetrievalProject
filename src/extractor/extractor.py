# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import json
import re

class CodeforcesExtractor:
	def process(self, html):
		problem={}
		head=html.find(class_='header')
		problem['title']=head.find(class_="title").string
		problem['memory_limit']=head.find(class_="memory-limit").find_all(text=True, recursive=False)[0]
		problem['time_limit']=head.find(class_="time-limit").find_all(text=True, recursive=False)[0]
		statement=html.find(class_='problem-statement').find_all('p')
		s = ""
		for p in statement:
			s = s + p.text
		problem['statement']=s
		return problem

class CodechefExtractor:
	def extract_label(self, html, label):
		pgs = html.find_all('p')
		for p in pgs:
			if p.find('label')!= None and p.find('label').text == label:
				return p.find('span').text
	def process(self, html):
		problem={}
		problem['title']=html.find_all('h1')[1].find_all(text=True, recursive=False)[0].strip()
		problem['time_limit']=self.extract_label(html, 'Time Limit:')
		problem['memory_limit']='1.5 GB'#its same for all in codechef
		full_statement=html.find(class_="problem-statement").find_all(recursive=False)
		print(full_statement)
		statement=""
		for p in full_statement:
			if(len(p.find_all('label'))>0):
				break
			statement = statement + ' '.join(p.find_all(text=True, recursive=True))
		problem['statement'] = statement
		return problem

class SpojExtractor:
	def get_td(self, html, label):
		trs=html.find_all('tr')
		for tr in trs:
			if len(tr.find_all('td'))==2 and tr.find_all('td')[0].text==label:
				return tr.find_all('td')[1].text.strip()
	def process(self, html):
		problem={}
		problem['title']=html.find(id="problem-name").string
		problem['memory_limit']=self.get_td(html, "Memory limit:")
		problem['time_limit']=self.get_td(html, "Time limit:")
		statement=' '.join(html.find(id="problem-body").find_all(text=True,recursive=True))
		problem['statement']=statement;
		return problem

class GeneralExtractor:
	def get_td(self, html, label):
		trs=html.find_all('tr')
		for tr in trs:
			if len(tr.find_all('td'))==2 and tr.find_all('td')[0].text==label:
				return tr.find_all('td')[1].text.strip()

	def take_out_judge(self, title):
		if "@" in title:
			return title.split('@')[0].strip()
		if len(title.split('-'))>1:
			return title.split('-')[-2].strip()
		return title

	def get_title(self,html):
		if html.find(id="problem-name") != None:
			return html.find(id="problem-name").string
		head=html.find(class_='header')
		if head != None and head.find(class_="title") != None:
			return head.find(class_="title").string
		if len(html.find_all('h1'))==2:
			return html.find_all('h1')[1].find_all(text=True, recursive=False)[0].strip()
		if html.head.title.text != "CS Academy":
			return self.take_out_judge(html.head.title.text)
		if len(html.find_all('h1'))==1:
			return html.find_all('h1')[0].find_all(text=True, recursive=False)[0].strip()

	def get_clear_title(self, html):
		title = self.get_title(html)
		if "." in title:
			title = title.split('.')[-1].strip()
		if ":" in title:
			title = title.split(':')[-1].strip()
		if "Problem " in title:
			return title.split("Problem ")[1]
		return title

	def get_text_time_limit(self, html):
		head=html.find(class_='header')
		if head != None and head.find(class_="time-limit")!=None:
			if len(head.find(class_="time-limit").find_all(text=True, recursive=False))>0:
				return head.find(class_="time-limit").find_all(text=True, recursive=False)[0]
		text=' '.join(html.find_all(text=True))
		match=re.search("([0-9]+\.)?[0-9]+ [sS]ec",text)
		if match!=None:
			return match.group(0)
		match=re.search("([0-9]+\.)?[0-9]+[sS]",text)
		if match!=None:
			return match.group(0)
		match=re.search('Test Time: \n( )*[0-9]+ MS',text)
		if match!=None:
			return match.group(0).split('\n')[1].strip()

	def get_time_limit(self,html):
		txt=self.get_text_time_limit(html)
		if txt==None:
			return -1
		match=re.search('([0-9]+\.)?[0-9]+',txt)
		val=eval(match.group(0))
		if val<100:
			val=val*1000
		return int(val)

	def get_text_memory_limit(self,html):
		#adding special case to Codechef, since all have same memory-limit
		#https://discuss.codechef.com/questions/93084/what-are-the-memory-limit-and-stack-size-on-codechef
		if(len(html.find_all(href="https://www.codechef.com/ide"))>0):
			return "1536 MB"
		head=html.find(class_='header')
		if head != None and head.find(class_="memory-limit")!=None:
			if len(head.find(class_="memory-limit").find_all(text=True, recursive=False))>0:
				return head.find(class_="memory-limit").find_all(text=True, recursive=False)[0]
		text=' '.join(html.find_all(text=True))
		match=re.search("Memory( )*([lL]imit)?( )*(.{5,5}( )*)?:( )*([0-9]+\.)?[0-9]+( )*[mM][bB]?",text)
		if match!=None:
			return match.group(0).split(":")[1].strip()

	def get_memory_limit(self,html):
		txt=self.get_text_memory_limit(html)
		if txt==None:
			return -1
		return eval(re.search('([0-9]+\.)?[0-9]+',txt).group(0))

	def extract(self, path, wpath=None):
		fl = open(path,"r")
		html = BeautifulSoup(fl, 'html.parser')
		problem = {}
		problem['title'] = self.get_clear_title(html)
		problem['time-limit'] = self.get_time_limit(html)
		problem['memory-limit'] = self.get_memory_limit(html)
		print(path, problem)
		if(wpath!=None):
			fp = open(wpath, 'w')
			json.dump(problem, fp)

extr=GeneralExtractor()

extr.extract("forces.html")
extr.extract("atcoder.html")
extr.extract("chef.html")
extr.extract("spoj.html")
extr.extract("dmoj.html")
extr.extract("a2oj.html")
extr.extract("csa.html")
extr.extract("timus.html")
extr.extract("coj.html")
extr.extract("uri.html")
