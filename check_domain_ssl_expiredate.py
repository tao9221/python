#!/usr/local/bin/python
#coding:utf8

import time
import sys
import re
import json
import requests
import whois
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('weixin/')
import weixin

def send(msg):
    token=weixin.get_accessToken()
    weixin.send(token,"xxxxxxxxx",msg)

def w_log(msg):
    with open('/var/log/checkssl.log','a+') as f:
        time_now = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write("{} - {}".format(time_now, msg))

def get_ssl_mesg(domain="baidu.com"):
    s = requests.session()
    datas = {'data':domain, 'type':'sslcheck', 'arg':'443'}
    url = 'http://web.chacuo.net/netsslcheck'
    d = s.post(url, data=datas)
    m = json.loads(d.content)['data'][0]
    res = re.compile(u"组织/公司名称：</td><td>(.*)</td></tr><tr><td>部门/单位.*颁发机构：</td><td>(.*)</td></tr><tr><td>证书详情.*证书类型：</td><td>(.*)</td></tr><tr><td>有效时间：</td><td>(.*)</td></tr><tr><td>过期时间：：</td><td>(.*)</td></tr><tr><td>多域名")
    result = re.findall(res, m)
    if len(result) > 0:
        last_days = re.findall(r'\d{1,}', result[0][4])[0]
        data = {
            "bfjg":result[0][1], 
            "gs":result[0][0], 
            "ym":domain, 
            "gqsj":last_days, 
            "yxsj":result[0][3], 
            "zslx":result[0][2],
            "runstat":1,
            }
    else:
        data = {"runstat":0}
    return data 

def get_domain_mesg(domain="baidu.com"):
    data = whois.whois(domain)
    run_stat = 0
    if data['expiration_date']:
        run_stat = 1
        last_time = (data['expiration_date']-datetime.datetime.now()).days
        status = ''
        if isinstance(data['status'],unicode):
            status = data['status'].split(' ')[0]
        elif isinstance(data['status'],list):
            status = data['status'][0]
        datas = {
            'ym':domain,
            'sqsj':data['creation_date'], 
            'yxsj':data['expiration_date'], 
            'gxsj':data['updated_date'],
            'gqsj':last_time, 
            'ymzt':status,
            'runstat':run_stat
            }
    else:
        datas = {'runstat':run_stat}
    return datas

def get_domain_list():
    file = './domain.txt'
    domain_list = []
    if file:
        with open(file) as f:
            domain_list.extend(f.readlines())
    return domain_list

def run():
    dm_list = get_domain_list()
    if len(dm_list) > 0:
        for dm in dm_list:
            dm = dm.strip()
            dm_msg = get_ssl_mesg(dm)
            dm_doamin = get_domain_mesg(dm)
            if dm_doamin['runstat'] == 1:
                if int(dm_doamin['gqsj']) < 30:
                    domain_data = '域名检测结果:\n域名:{ym}\n申请时间:{sqsj}\n更新时间:{gxsj}\n过期时间:{yxsj}\n有效时间:还有 {gqsj} 天过期\n域名状态:{ymzt}\n'.format(**dm_doamin) 
                    send(domain_data)
                    w_log('域名检测:{}:{}!!!!!!!!\n'.format(dm,dm_doamin['gqsj']))
                else:
                    w_log('域名检测:{}:{}\n'.format(dm,dm_doamin['gqsj']))
            if dm_msg['runstat'] == 1:
                if int(dm_msg['gqsj']) < 60:
                    ssl_data = 'SSL证书检测结果:\n域名:{ym}\n公司:{gs}\n有效时间:{yxsj}\n过期时间:还有 {gqsj} 天过期\n证书类型:{zslx}\n颁发机构:{bfjg}\n'.format(**dm_msg)
                    send(ssl_data)
                    w_log(w_log('SSL证书检测:{}:{}!!!!!!!!\n'.format(dm,dm_msg['gqsj'])))
                else:
                    w_log('SSL证书检测:{}:{}\n'.format(dm,dm_msg['gqsj']))

if __name__ == "__main__":
    run()

