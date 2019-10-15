#!/usr/local/python3.6/bin/python
#coding:utf-8

import sys
import os
from exchangelib import Credentials, Account

sys.path.append('weixin/')
import weixin

order_all_number = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'order_number.txt')
username = 'xxxx@mail.cn'
password = 'xxxx'

try:
    credentials = Credentials(username, password)
    account = Account(username, credentials=credentials, autodiscover=True)

except Exception as e:
    print('错误: {0}'.format(e))
    os.exit(1)

def send(msg):
    token=weixin.get_accessToken()
    weixin.send(token,"@all",msg)

def order_mail_number():
     filter_str='工单'
     order_number=account.inbox.children.filter(subject__icontains=filter_str).count()
     return order_number

def handle_mail(number=1):
    data_mail = {}
    account.inbox.refresh()
    for mail in account.inbox.children.filter(subject__icontains='工单').order_by('-datetime_received')[:number]:
        if "SRE" in mail.text_body:
            data_mail[mail.subject.split('---')[1]] = mail.text_body
    return data_mail

def diff_number():
    new_mail_number = order_mail_number()
    if not os.path.isfile(order_all_number):
        with open(order_all_number, 'w') as f:
            f.write(str(new_mail_number))
    else:
        with open(order_all_number, 'r') as f:
            old_number = f.readlines()[0]
        with open(order_all_number, 'w') as f:
            f.write(str(new_mail_number))
    return int(new_mail_number)-int(old_number)

def run():
    diffnumber = diff_number() 
    if diffnumber == 0: sys.exit(0)
    data = handle_mail(number=diffnumber)
    if len(data) != 0:
        huali = '='
        datas = "待处理工单:\n"
        for k,v in data.items():
            datas = "{0}\n{1}\n{2}\n{3}".format(datas, huali*25, k, v)
        send(datas)

if __name__ == "__main__":
    run()
