import urllib2
import sys,os
import json
import time,datetime

reload(sys)
sys.setdefaultencoding('utf8')

def get_accessToken():
    corpid="xxxxxxxx"
    secret="xxxxxxxx"
    con_url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(corpid,secret)
    try:
        if os.path.exists("token"):
            token,expire,oldtime=file("/tmp/token.txt").read().split()
            if time.time()-float(oldtime) < float(expire):
                return token
        rst=urllib2.urlopen(con_url)
        dic=json.loads(rst.read())
        token=dic['access_token']
        expire=dic['expires_in']
        t=time.time()
        file("/tmp/token.txt","w").write("%s %s %s"%(token,expire,t))
        return token

    except BaseException ,e:
        file("/tmp/log.txt","a").write("%s %s\n"%(datetime.datetime.now(),e))
        return None
def send(token,uid,msg):
    token=token
    userid=uid
    msg=msg
    url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s"%token
    d={"touser":userid,
        "msgtype":"text",
        'agentid':"1000003",
        "text":{ 
            "content":msg
        }
    }
    d=json.dumps(d,ensure_ascii=False)
    d=d.encode("utf8")
    rst=urllib2.urlopen(url,data=d).read()
    file("/tmp/log.txt","a").write("%s %s\n"%(datetime.datetime.now(),rst))
    
if __name__=="__main__":
    token=get_accessToken()
    msg=sys.argv[1]
    send(token,"xxxxxxxxxx",msg)

