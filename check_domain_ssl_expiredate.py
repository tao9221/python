#!/usr/local/bin/python
#coding:utf8

import time
import sys
import os
import re
import json
import requests
import whois
import time
import datetime
from multiprocessing import Process, Pool

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'weixin/'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'whois'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mail'))
logFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'logCheck.log')
import weixin
import mail

def send(msg):
    token=weixin.get_accessToken()
    weixin.send(token,"15601119330",msg)

def send_mail(message):
    data = {}
    data['to'] = 'sre@163.com'
    data['title'] = '过期域名或者证书监测'
    data['message'] = message.replace('\n','<br \>')
    url = 'http://10.58.165.166:8866/sendmail'
    try:
        requests.post(url, data=data)
    except Exception, e:
        w_log('{0} send mail error\n'.format(message))

def w_log(msg):
    with open(logFile,'a+') as f:
        time_now = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write("{} - {}".format(time_now, msg))

def get_ssl_mesg(domain="baidu.com"):
    s = requests.session()
    datas = {'data':domain, 'type':'sslcheck', 'arg':'443'}
    url = 'http://web.chacuo.net/netsslcheck'
    try:
        d = s.post(url, data=datas, timeout=120)
        m = json.loads(d.content)['data'][0]
    except Exception, e:
        w_log('{0} curl ssl web error\r\n'.format(domain))
        return {} 
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
    s.close()
    return data 

def get_domain_mesg(domain="baidu.com"):
    try:
        data = whois.whois(domain)
        time.sleep(1)
    except:
        w_log("{0} whois error.\r\n".format(domain))
        return {}
    run_stat = 0
    if data['expiration_date']:
        run_stat = 1
        status = ''
        if isinstance(data['status'],unicode):
            status = data['status'].split(' ')[0]
        elif isinstance(data['status'],list):
            status = data['status'][0]
        if isinstance(data.get('expiration_date'),list):
            last_time = (data.get('expiration_date')[0]-datetime.datetime.now()).days
        else:
            last_time = (data.get('expiration_date')-datetime.datetime.now()).days
        if isinstance(data.get('creation_date'),list):
            data['creation_date'] = data.get('creation_date')[0]
        if isinstance(data.get('expiration_date'),list):
            data['expiration_date'] = data.get('expiration_date')[0]
        if isinstance(data.get('updated_date'),list):
            data['updated_date'] = data.get('updated_date')[0]
        
        datas = {
            'ym':domain,
            'sqsj':data.get('creation_date','无信息'),
            'yxsj':data.get('expiration_date','无信息'), 
            'gxsj':data.get('updated_date','无信息'),
            'gqsj':last_time, 
            'ymzt':status,
            'runstat':run_stat
            }
    else:
        datas = {'runstat':run_stat}
    return datas

def get_domain_list():
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'domain.txt')
    domain_list = []
    if file:
        with open(file) as f:
            for l in f.readlines():
                if not l.startswith('#'):
                    domain_list.append(l)
    return domain_list

def check_ssl(dm):
    dm_msg = get_ssl_mesg(dm)
    if dm_msg.get('runstat',0) == 1:
        if int(dm_msg['gqsj']) < 60:
            ssl_data = 'SSL证书检测结果:\n域名:{ym}\n公司:{gs}\n有效时间:{yxsj}\n过期时间:还有 {gqsj} 天过期\n证书类型:{zslx}\n颁发机构:{bfjg}\n'.format(**dm_msg)
            send(ssl_data)
            send_mail(ssl_data)
            w_log('SSL证书检测:{}:{}!!!!!!!!\n'.format(dm,dm_msg['gqsj']))
        else:
            w_log('SSL证书检测:{}:{}\n'.format(dm,dm_msg['gqsj']))

def check_domain(dm):
    dm_domain = get_domain_mesg(dm)
    if dm_domain.get('runstat',0) == 1:
        if int(dm_domain['gqsj']) < 30:
            domain_data = '域名检测结果:\n域名:{ym}\n申请时间:{sqsj}\n更新时间:{gxsj}\n过期时间:{yxsj}\n有效时间:还有 {gqsj} 天过期\n域名状态:{ymzt}\n'.format(**dm_domain)
            send(domain_data)
            send_mail(domain_data)
            w_log('域名检测:{}:{}!!!!!!!!\n'.format(dm,dm_domain['gqsj']))
        else:
            w_log('域名检测:{}:{}\n'.format(dm,dm_domain['gqsj']))

def run():
    dm_list = get_domain_list()
    domain_ssl = []
    domain_dm = []
    start = time.time()
    if len(dm_list) > 0:
        pool = Pool()
        for dm in dm_list:
            dm = dm.strip()
            if 'https' in dm:
                dm = dm.replace('https://','')
                domain_dm.append(dm)
                pool.apply_async(check_ssl, args=(dm,))
            else:
                domain_dm.append(dm)
        pool.close()
        pool.join() 
    for dm in domain_dm:
        check_domain(dm)
    end = time.time()
    w_log("本次运行使用时间: {0} 秒\n".format(end-start))

if __name__ == "__main__":
    run()
