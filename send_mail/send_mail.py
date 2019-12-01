from flask import Flask, request
import sys
import time

sys.path.append('mail_exchange.py')
import mail_exchange

app = Flask(__name__)

def wlog(msg):
    with open('./mail.log','a') as f:
        f.write("{0} - {1}\n".format(time.strftime('%F_%T'), msg))

@app.route('/')
def hello_world(test):
    return 'hello world %s'%test

@app.route('/sendmail', methods=['POST'])
def send_email():
    to = request.values.get('to', 'xxx@xxx.com.cn')
    title = request.values.get('title', '默认title')
    message = request.values.get('message', '默认消息')
    try:
        mail_exchange.send_email(title, to, message)
        wlog("{0} | {1} | {2}.".format(to, title, message))
    except Exception as e:
        return '邮件发送失败,错误:%s'%e
    return '邮件发送成功.'

if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=8866, debug=True)
    app.run(host='0.0.0.0',port=8866)
