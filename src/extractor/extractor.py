
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4.element import Comment
import json
import re

class GeneralExtractor:
	def tag_visible(self,element):
		if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
			return False
		if isinstance(element, Comment):
			return False
		return True

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

	def get_props(self,html):
		txt=' '.join(filter(self.tag_visible,html.find_all(text=True,recursive=True)))
		pattern="([a-zA-Z]+( )?){1,2}\:"
		pattern=pattern+"([ \n])*"  +  "([A-Za-z0-9\.]+( )?){1,2}"
		pattern="("+pattern+")"
		rfe=re.findall(pattern,txt)
		if rfe==None:
			return None
		ret={}
		for grp in rfe:
			if(grp!=None and len(grp[0].split(':'))==2):
				ret[grp[0].split(':')[0]]=grp[0].split(':')[1]
		return ret

	def get_statement(self,html):
		text=' '.join(html.find_all(recursive=True,text=True))
		ps = html.find_all('p')
		if(html.find(class_='problem-statement')!=None):
			psar=html.find(class_='problem-statement')
			return ' '.join([' '.join(psar.find_all(text=True,recursive=True)) for x in ps])
		prestatement = ' '.join([' '.join(x.find_all(text=True,recursive=True)) for x in ps])
		return prestatement

	def extract(self, path, wpath=None):
		fl = open(path,"r", encoding="utf8")
		html = BeautifulSoup(fl, 'html.parser')
		problem = {}
		problem['title'] = self.get_clear_title(html)
		problem['time-limit'] = self.get_time_limit(html)
		problem['memory-limit'] = self.get_memory_limit(html)
		problem['props'] = self.get_props(html)
		problem['statement'] = self.get_statement(html)
		if(wpath!=None):
			fp = open(wpath, 'w')
			json.dump(problem, fp)

extr=GeneralExtractor()

