#coding:utf8
from HTMLParser import HTMLParser
import requests
import re

def _attr(attrs, attrname):
	for attr in attrs:
		if attr[0] == attrname:
			return attr[1]
	return None

class PoemParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.in_div = False
		self.in_a = False
		self.tangshi_list = []
		self.pattern = re.compile(r'(.+)')
		self.current_poem = {}

	def handle_starttag(self, tag, attrs):
		if tag == 'div' and _attr(attrs, 'class') == 'typecont':
			self.in_div = True
		if tag == 'div' and _attr(attrs, 'class') == 'right':
		    self.in_div = False

		if self.in_div and tag == 'a':
			self.in_a = True
			self.current_poem['url'] = _attr(attrs, 'href')

	def handle_endtag(self, tag):
		if tag == 'a':
			self.in_a = False

	def handle_data(self, data):
		if self.in_a:
			#print(data)
			m = self.pattern.match(data)
			if m:
				self.current_poem['title'] = m.group(1)
				self.tangshi_list.append(self.current_poem)
				self.current_poem = {}

def retrive_tangshi_300():
	url = 'http://so.gushiwen.org/gushi/tangshi.aspx'
	r = requests.get(url)
	p = PoemParser()
	p.feed(r.content)
	return p.tangshi_list

if __name__ == '__main__':
	l = retrive_tangshi_300()
	print('total %d poems' %len(l))
	for i in range(10):
		print('标题:{0:#<15} URL:{1:<}'.format(l[i]['title'], l[i]['url']))
			
