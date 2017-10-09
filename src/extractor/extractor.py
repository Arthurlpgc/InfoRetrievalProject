from bs4 import BeautifulSoup

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

class GeneralExtractor:
	def is_codeforces(self, html):
		prop = html.find(property="og:site_name")
		if prop == None:
			return False
		return prop['content']=="Codeforces"

	def extract(self, path):
		fl = open(path,"r")
		html = BeautifulSoup(fl, 'html.parser')
		extractor = {}
		if self.is_codeforces(html):
			extractor = CodeforcesExtractor()
		else:
			extractor = CodechefExtractor()
		problem = extractor.process(html)
		print(problem)

extr=GeneralExtractor()

extr.extract("a.html")
extr.extract("b.html")
extr.extract("chef.html")
