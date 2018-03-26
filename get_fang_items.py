#!/usr/bin/python
#coding:utf8

from selenium import webdriver
import weixin
import os

os.environ.update({'PATH':'/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/root/code/phantomjs-2.1.1-linux-x86_64/bin/'})
driver = webdriver.PhantomJS('phantomjs')

def send(msg):
	token=weixin.get_accessToken()
	weixin.send(token,"iphone_number_xxxxx",msg)

def get_text(url):
	url='http://www.bphc.com.cn/front/noroomstaff/planLists'
	driver.get(url)
	d=driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div/h2')
	return d.text 

def vs(url):
	with open('/root/test/fang/txt','r') as f:
		text=f.readline()
	new_text = get_text(url)
	if str(new_text) != str(text):
		send('url:{} | {}'.format(url,new_text))
		with open('/root/test/fang/txt', 'w') as f:
			f.write(new_text)

url = 'http://www.bphc.com.cn/front/noroomstaff/planLists'
vs(url)
driver.quit()

