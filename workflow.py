#!/usr/bin/env python
#coding: utf-8

import datetime
import time
import requests

xingqi = {0:'星期日', 1:'星期一', 2:'星期二', 3:'星期三', 4:'星期四', 5:'星期五', 6:'星期六'}
sre = ['人员1', '人员2', '人员3', '人员4', '人员5‘, '人员6', '人员7']

def run(start, end, day, datas, xinqi, sre):
    now = datetime.datetime.now()
    for i in range(start, end):
        if day > 6:
            news_x = i
            with open('number', 'w') as f:
                f.write(str(news_x))
            return [start, end, day, datas]
        key = datetime.datetime.strftime(now+datetime.timedelta(days=day),'%F')
        xqdays = xingqi.get(int(datetime.datetime.strftime(now+datetime.timedelta(days=day),'%w')))
        datas[key] = [sre[i-1], xqdays]
        day += 1
    return [start, end, day, datas]

def send_mail(message):
    data = {}
    data['to'] = 'xxx@mail.cn'
    data['title'] = '值班表'
    data['message'] = message.replace('\n','<br \>')
    url = 'http://1.1.1.1:8866/sendmail'
    try:
        requests.post(url, data=data)
    except Exception, e:
        print("Error: {}".format(e)) 


if __name__ == '__main__':
    html = '<table border="2" bordercolor="black" cellspacing="0" cellpadding="5"><tr><th colspan="4">值班表</th><tr><th>星期</th><th>日期</th><th>值班人员</th><th>值班计划</th></tr>'
    day = 0
    datas = {}
    with open('number') as f:
        start = int(f.readlines()[0])
    run_one = run(start, len(sre)+1, day, datas, xingqi, sre)
    run_two = run(1, start, run_one[2], run_one[3], xingqi, sre)
    datas = run_two[3]
    for k,v in sorted(datas.iteritems(), key=lambda d:d[0], reverse=False): 
        print('{0} | {1} | {2}'.format(v[1], k, v[0].strip())) 
        html += '<tr><td>{}</td><td>{}</td><td>{}</td><td>正常</td></tr>'.format(v[1], k, v[0].strip())
        with open('work.log', 'a') as f:
            f.write('{} - {} | {} {}\n'.format(time.strftime('%F_%T',time.localtime()), k, v[1], v[0].strip()))
    html += '</table>'
    send_mail(html)

    if len(sre) == 7:
        with open('number', 'w') as f:
            f.write(str((start+1)%7))
