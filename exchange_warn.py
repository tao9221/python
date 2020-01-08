#!/usr/local/python3.6/bin/python3
#coding:utf-8

import sys
import os
from exchangelib import DELEGATE, Credentials, Account, Message, Mailbox, HTMLBody, Configuration

sys.path.append('/app/script/monitor/')
import weixin

order_all_number = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'order_number.txt')
username = 'abc@123.com'
password = 'pwd'
r_server = 'owa.corp.mail.cn'

try:
    credentials = Credentials(username, password)
    config = Configuration(server=r_server, credentials=credentials)
    account = Account(username, autodiscover=False, config=config, access_type=DELEGATE)

except Exception as e:
    print('错误: {0}'.format(e))
    sys.exit(1)

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
    for mail in account.inbox.children.filter(subject__icontains='工单ID').order_by('-datetime_received')[:number]:
        if "SRE" in mail.text_body or "应用搭建" in mail.text_body or "Nginx接入" in mail.text_body:
            try:
                key = mail.subject.split('---')[1]
                data_mail[key] = mail.text_body
            except:
                pass
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
