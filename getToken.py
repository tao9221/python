#coding:utf8
import time
import struct
import hmac
import hashlib
import base64

def generate_code(secretkey, value=None):
    value = value or int(time.time() / 30)
    value = struct.pack('>q', value)
    secretkey = base64.b32decode(secretkey.upper())
    hash = hmac.new(secretkey, value, hashlib.sha1).digest()
    offset = ord(hash[-1]) & 0x0F
    truncated_hash = hash[offset:offset + 4]
    truncated_hash = struct.unpack('>L', truncated_hash)[0]
    truncated_hash &= 0x7FFFFFFF
    truncated_hash %= 1000000
    return '%06d' % truncated_hash

class OTP:
    def __init__(self, secret="",):
        self.secret = secret
       
    def hotp(self, counter):    
        basedSecret = base64.b32decode(self.secret, True)    
        structSecret = struct.pack(">Q", counter)    
        hmacSecret = hmac.new(basedSecret, structSecret, hashlib.sha1).digest()    
        ordSecret = ord(hmacSecret[19]) & 15    
        tokenSecret = (struct.unpack(">I", hmacSecret[ordSecret:ordSecret+4])[0] & 0x7fffffff) % 1000000    
        return tokenSecret
    def totp(self, period=30):
        counter = int(time.time()) # period
        return self.hotp(counter + offset)


key = "1e13ddf1a6d6eab171bd70461e197720fc36d004"


print generate_code('EFHO7YYFEU7XBNP7'),'天津'
print generate_code('IYH7ZJ2ANI2R2MWN'),'北京'
