#!/usr/local/bin/python
#coding:utf8

from bs4 import BeautifulSoup
import requests
import weixin
import os

os.environ.update({'PATH':'/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/home/qinjuntao/bin'})

def send(msg):
    token=weixin.get_accessToken()
    weixin.send(token,"xxxxxx",msg)

def get_text(url):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, "lxml")
    d = soup.select("body > div:nth-of-type(2) > div > div.planContent > div.noList.orally > div > h2")
    return d[0].get_text() 

def vs(url):
    dirfile = "txt"
    with open(dirfile ,'r') as f:
        text=f.readline()
    new_text = get_text(url)
    new_text = new_text.encode("utf8")
    if str(new_text) != str(text):
        send('url:{} | {}'.format(url,new_text))
        with open(dirfile, 'w') as f:
            f.write(new_text)

url = 'http://www.bphc.com.cn/front/noroomstaff/planLists'
vs(url)

