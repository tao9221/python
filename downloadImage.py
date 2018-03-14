#coding:utf8

import requests
import urllib
import os
import threading

gImageList = []
gCondition = threading.Condition()

class Producer(threading.Thread):
	def run(self):
		global gImageList
		global gCondition
		imgs = download_wallpaper_list()
		gCondition.acquire()
		for i in imgs:
			if 'imageUrl' in i:
				gImageList.append(i['imageUrl'])
		print('%s: left:%d' %(threading.current_thread, len(gImageList)))
		gCondition.notify_all()
		gCondition.release()

class Consumer(threading.Thread):
	def run(self):
		while True:
			global gImageList
			global gCondition
	
			gCondition.acquire()
			print('%s: try download, pool:%d' %(threading.current_thread,len(gImageList)))
			while len(gImageList) == 0:
				print('%s: wait, pool:%d' %(threading.current_thread, len(gImageList)))
				gCondition.wait()
			url = gImageList.pop()
			gCondition.release()
			_download_image(url)

def _download_image(url, folder='image'):
	if not os.path.isdir(folder):
		os.mkdir(folder)
	print('downloading %s' %url)

	def _fname(s):
		return os.path.join(folder, os.path.split(url)[1])

	urllib.urlretrieve(url, _fname(url))

def download_wallpaper_list():
	url = 'http://image.baidu.com/data/imgs'
	params = {
		'pn': 1,
		'rn': 200,
		'col': '壁纸',
		'tag': '美女',
		'tag3': '',
		'width': 1600,
		'height': 900,
		'ic': 0,
		'ie': 'utf8',
		'oe': 'utf08',
		'image_id': '',
		'fr': 'channel',
		'p': 'channel',
		'from': 1,
		'app': 'img.browser.channel.wallpaper',
		't': '0.016929891658946872'
	}
	r = requests.get(url, params=params)
	imgs = r.json()['imgs']
	print('%s: total %d imgs' %(threading.current_thread, len(imgs)))
	return imgs

if __name__ == '__main__':
	Producer().start()

	for i in range(5):
		Consumer().start()
