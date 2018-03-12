#/usr/local/python2.7/bin/python
#coding:utf-8

import json
import time
from websocket import create_connection
import requests

def Getprice(url, data):
    ws = create_connection(url, timeout=5)
    ws.send(json.dumps(data))
    odata = ws.recv()
    odata = ws.recv()
    
    ndata = json.loads(odata)
    lastprice = ndata[0].get('data').get('last')
    if isinstance(lastprice, int) or isinstance(lastprice, float): 
        return lastprice
    else:
        return 0.00

def Postdata(lastprice):
    today = time.strftime('%Y-%m-%d')
    data = {
	    "id":2,
	    "val": lastprice,
	    "key": "price",
	    "statment_date": today
	}
    r = requests.post("http://1.1.1.1:8000/statement/add/", data=data, timeout=5)
    if r.status_code != '200':
        print 'post data error.'

if __name__ == '__main__':
    url = 'wss://real.okcoin.cn:10440/websocket/okcoinapi'
    data = {'event':'addChannel','channel':'ok_sub_spotcny_btc_ticker'}
    lastprice = Getprice(url, data)
    print lastprice
    #Postdata(lastprice)
