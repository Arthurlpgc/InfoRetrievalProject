from bs4 import BeautifulSoup
import json

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
	def is_codeforces(self, html):
		prop = html.find(property="og:site_name")
		if prop == None:
			return False
		return prop['content']=="Codeforces"
	
	def is_codechef(self, html):
		return len(html.find_all(href="https://www.codechef.com/ide"))>0

	def is_uri(self, html):
		return False
		
	def is_spoj(self, html):
		prop = html.find(property="og:site_name")
		if prop == None:
			return False
		return prop['content']=="spoj.com"

	def extract(self, path, wpath="result.json"):
		fl = open(path,"r")
		html = BeautifulSoup(fl, 'html.parser')
		extractor = {}
		if self.is_codeforces(html):
			extractor = CodeforcesExtractor()
		elif self.is_codechef(html):
			extractor = CodechefExtractor()
		elif self.is_uri(html):
			print("Not done yet")
		elif self.is_spoj(html):
			extractor = SpojExtractor()
		else:
			print("Error")
		problem = extractor.process(html)
		print(problem)
		fp = open(wpath, 'w')
		json.dump(problem, fp)

extr=GeneralExtractor()

extr.extract("a.html")
extr.extract("b.html")
extr.extract("chef.html")
extr.extract("spoj.html")

