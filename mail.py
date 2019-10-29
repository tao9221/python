#!/usr/bin/env python
#coding=utf-8

import smtplib
from email.header import Header
from email.mime.text import MIMEText
import sys 

mail_host = 'smtp.163.com'
mail_user = 'xxx@163.com'
mail_pass = 'xxx'

sender = 'linuxtao@163.com'
def send_email(title='报警邮件',recervers=['xxx@qq.com'],msg='content'):
    #message = MIMEText(msg, 'plain', 'utf-8')
    message = MIMEText(msg, 'html', 'utf-8')
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(recervers)
    message['Subject'] = title
    
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, recervers, message.as_string())
        print("mail has been send successfully.")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "usage:%s title mail1,mail2 message"%sys.argv[0]
        sys.exit()
    titles = sys.argv[1]
    recerverss = sys.argv[2]
    message = sys.argv[3]
    send_email(title=titles,recervers=[recerverss],msg=message)
