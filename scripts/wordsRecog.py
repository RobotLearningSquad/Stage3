#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib2
import time
import urllib
import json
import hashlib
import base64


def main():
    f = open("./static/audio/hts0000f2e1@ch09280e6320d4477500.wav", 'rb')
    file_content = f.read()
    print len(file_content)
    base64_audio = base64.b64encode(file_content)
    print len(base64_audio)
    body = urllib.urlencode({'audio': base64_audio})
    print len(body);

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = 'f9f0ad524f7d44cee5ab04546c7894b1'
    param = {"engine_type": "sms16k", "aue": "raw"}

    x_appid = '5b077b83'
    x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib2.Request(url, body, x_header)
    result = urllib2.urlopen(req)
    result = result.read()
    print result
    return

if __name__ == '__main__':
    main() 
