#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib2
import time
import urllib
import json
import hashlib
import base64
import re
import json


def main(msg):


    startPos = msg.find("data") + 7
    print msg[startPos]
    endPos = msg.find("\"",startPos)-1
    print msg[endPos]
    info = msg[startPos:endPos]
    midInfo = info.find("，".decode('utf-8'))
    if midInfo == -1:
        midInfo = info.find("。".decode('utf-8'))
   

    # info = "存入苹果13个，12天后过期。".decode('utf-8')

    page = -1
    num = -1
    day = -1
    food = ""
    page = -1
    dateLeft = -1
    unit = ""

    # detect command
    infoLen = len(info)
    if infoLen == 4:
        if info[0] == '查'.decode('utf-8'):
            page = 10
        elif info[0] == '存'.decode('utf-8') or (info[0] == '传'.decode('utf-8')):
            page = 11
        elif info[0] == '取'.decode('utf-8'):
            page = 12
        resultReturn = {'page':page,'num':num, 'dateLeft':dateLeft, 'food':food,  'unit':unit}
        print json.dumps(resultReturn, encoding='UTF-8', ensure_ascii=False)
        return json.dumps(resultReturn, encoding='UTF-8', ensure_ascii=False)

   
    
    bigFlag = 1
    #when num / day < 10
    # change Chinese into ASCII 一二三四五六七八九十
    for x in info[0:midInfo]:
        if x=='一'.decode('utf-8'):
            num=1
            bigFlag = 0
        elif x=='二'.decode('utf-8'):
            num=2
            bigFlag = 0
        elif x=='三'.decode('utf-8'):
            num=3
            bigFlag = 0
        elif x=='四'.decode('utf-8'):
            num=4
            bigFlag = 0
        elif x=='五'.decode('utf-8'):
            num=5
            bigFlag = 0
        elif x=='六'.decode('utf-8'):
            num=6
            bigFlag = 0
        elif x=='七'.decode('utf-8'):
            num=7
            bigFlag = 0
        elif x=='八'.decode('utf-8'):
            num=8
            bigFlag = 0
        elif x=='九'.decode('utf-8'):
            num=9
            bigFlag = 0
        elif x=='十'.decode('utf-8'):
            num=10
            bigFlag = 0
    for x in info[midInfo:len(info)]:
        if x=='一'.decode('utf-8'):
            day=1
        elif x=='二'.decode('utf-8'):
            day=2
        elif x=='三'.decode('utf-8'):
            day=3
        elif x=='四'.decode('utf-8'):
            day=4
        elif x=='五'.decode('utf-8'):
            day=5
        elif x=='六'.decode('utf-8'):
            day=6
        elif x=='七'.decode('utf-8'):
            day=7
        elif x=='八'.decode('utf-8'):
            day=8
        elif x=='九'.decode('utf-8'):
            day=9
        elif x=='十'.decode('utf-8'):
            day=10
    # 数字数量大于10
    ret2 = re.findall('\d+', info)
    print ret2
    index = 0
    if num == -1:
        num = ret2[index]
        index=index+1
    if  day == -1:
        day = ret2[index]

    unit = info[midInfo-1]

    if bigFlag==0:
        food = info[2:midInfo-2]
    elif bigFlag==1:
        numstr = str(num)
        strlen = len(numstr)
        food = info[2:midInfo-strlen-1]

    dateLeft = int(day)*24

    # detect next jump
    if info[0] == '查'.decode('utf-8'):
            page = 20
    elif info[0] == '存'.decode('utf-8') or (info[0] == '传'.decode('utf-8')):
            page = 21
    elif info[0] == '取'.decode('utf-8'):
            page = 22


    resultReturn = {'page':page,'num':num, 'dateLeft':dateLeft, 'food':food,  'unit':unit}

    finalInfo = json.dumps(resultReturn, encoding='UTF-8', ensure_ascii=False)

    print "finalInfo=="
    print finalInfo

    return finalInfo


if __name__ == '__main__':
    msg = "{\"code\":\"0\",\"data\":\"存入苹果12个，四天后过期。\",\"sid\":\"zat00000009@ch0fc40d9e4cdf000100\",\"desc\":\"success\"}".decode('utf-8')
    main(msg) 
