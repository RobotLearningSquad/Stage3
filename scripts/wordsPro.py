#-*- coding: utf-8 -*-
import requests
import re
import time
import hashlib
import base64
import struct

URL = "http://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"
APPID = "5b077b83"
API_KEY = "8e21826208a1503d5c3e5d19028e3eff"

def getHeader():
        curTime = str(int(time.time()))
        param = "{\"aue\":\""+AUE+"\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"
        paramBase64 = base64.b64encode(param)
        m2 = hashlib.md5()
        m2.update(API_KEY + curTime + paramBase64)
        checkSum = m2.hexdigest()
        header ={
                'X-CurTime':curTime,
                'X-Param':paramBase64,
                'X-Appid':APPID,
                'X-CheckSum':checkSum,
                'X-Real-Ip':'127.0.0.1',
                'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

def getBody(text):
        data = {'text':text}
        return data

def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    f.close()

r = requests.post(URL,headers=getHeader(),data=getBody("存入苹果14个，122天后过期"))
contentType = r.headers['Content-Type']
if contentType == "audio/mpeg":
    sid = r.headers['sid']
    if AUE == "raw":
        writeFile("./static/audio/"+"apple4"+".wav", r.content)
    else :
        writeFile("./static/audio/"+sid+".mp3", r.content)
    print "success, sid = " + sid
else :
    print r.text 