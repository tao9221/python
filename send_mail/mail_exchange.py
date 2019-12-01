#!/usr/local/python3.6/bin/python3
#coding:utf-8

import sys
from exchangelib import DELEGATE, Credentials, Account, Message, Mailbox, HTMLBody, Configuration

username = 'xxx@xxx.com.cn'
password = 'xxx'
r_server = 'owa.corp.xxx.com.cn'

def send_email(title='报警邮件',recervers='xxx@qq.com',msg='content'):
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
        to_recipients = [Mailbox(email_address=recervers)]
    )
    m.send()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage:%s title mail1,mail2 message"%sys.argv[0])
        sys.exit()
    titles = sys.argv[1]
    recerverss = sys.argv[2]
    message = sys.argv[3]
    send_email(title=titles,recervers=recerverss,msg=message)
