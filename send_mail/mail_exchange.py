#!/usr/local/python3.6/bin/python3
#coding:utf-8

import sys
import os
from exchangelib import DELEGATE, Credentials, Account, Message, Mailbox, HTMLBody, Configuration, FileAttachment

username = 'xxx@mail.com'
password = 'pwd'
r_server = 'owa.corp.mail.com'

def send_email(title='报警邮件',recervers='xxxx@qq.com',msg='content', file_name=''):
    try:
        credentials = Credentials(username, password)
        config = Configuration(server=r_server, credentials=credentials)
        account = Account(username, autodiscover=False, config=config, access_type=DELEGATE)
    
    except Exception as e:
        print('错误: {0}'.format(e))
        sys.exit(1)

    m = Message(
        account = account,
        subject=title,
        body=HTMLBody(msg),
        to_recipients = [Mailbox(email_address=x) for x in recervers.split(',')]
    )
    if file_name:
        with open(os.path.abspath(r"../work_flow/sre.xls"), "rb") as f:
            cont = f.read()
        attchF = FileAttachment(name='值班表.xls', content=cont)
        m.attach(attchF)
        m.send_and_save()
    else:
        m.send()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage:%s title mail1,mail2 message"%sys.argv[0])
        sys.exit()
    titles = sys.argv[1]
    recerverss = sys.argv[2]
    message = sys.argv[3]
    send_email(title=titles,recervers=recerverss,msg=message)
    #send_email(title="baojing",recervers="xxx@mail.com",msg="diyifeng", file_name='sre')
