#!/usr/bin/env python
# -*- coding=utf-8 -*-
from werkzeug.utils import secure_filename
from flask import *
from flask_pymongo import PyMongo
import logging
import os
import time
import bson
import wordsRecog 
import wave
#from robo_talker import talker 
# index/
# command/        GET
  # put/          GET
    # upload/     POST
  # change/       GET
    # upload/     PUT
  # show/         GET
  # successed/    GET
  # failed/       GET
#| 100 |	Continue | |
#| 200 |	OK | |
#| 201 |	Created | database item created|
#| 304 |	Not Modified | nothing changed|
#| 400 |	Bad Request | can't deal with|
#| 403 |	Forbidden |	file name wrong |
#| 404 |	Not Found |	no pages |
#| 408 |	Request Time-out |	|
#| 414 |	Request-URI Too Large | |
#| 500 |	Internal Server Error | |

    #debug
    #ticks = time.time()
    #localtime = time.localtime(time.time())
    #userid='0.0.0.0'
    #food= 'apple'
    #num= 3
    #unit='one'
    #date=ticks
    #dateLeft= 10
    #frage1 = {'userid':userid, 'food':food, 'num':int(num), 'unit':unit, 'date':date, 'dateLeft':int(dateLeft)}
    #frage2 = {'userid':'0.0.0.1', 'food':food, 'num':int(num), 'unit':unit, 'date':date, 'dateLeft':int(dateLeft)}
    #frage3 = {'userid':userid, 'food':'toufu', 'num':int(num), 'unit':unit, 'date':date, 'dateLeft':int(dateLeft)}
    #mongo.db.frages.insert_one(frage1)
    #addDB(userid,food,num,unit,date,dateLeft)
    #mongo.db.frages.insert_one(frage3)
    #res = queryDB(userid, food)
    #print res

    #res = changeDB(userid, food, 5, True)
    #print res

    #res = queryDB(userid, food)
    #print res

    #res = deleteDB(userid, food)
    #print res

    #res = queryDB(userid, None)
    #print res

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Session key'
app.config['FLASK_DEBUG'] = 1
app.config.update(
    MONGO_HOST='localhost',
    MONGO_PORT = 27017,
    MONGO_URI='mongodb://localhost:27017/frage_DB',
    MONGO_USERNAME='tempo',
    MONGO_PASSWORD='11111111',
    MONGO_DBNAME='frage_DB'
)
mongo = PyMongo(app)
PageCount = 0

class  Fridge(object):
    def __init__(self, food, num, unit,date, leftHour):
        self.food = food
        self.num = num
        self.unit = unit
        self.date = date
        self.leftHour = leftHour
    
# item can be None
# return food List
def queryDB(userid, item):
    foodlist = []
    if userid is not None:
        if item is not None:
            frage = mongo.db.frages.find({'userid':userid, 'food':item})
        else:
            frage = mongo.db.frages.find({'userid':userid})
        for food in frage:
            food.pop('_id')
            foodlist.append(food)
    return foodlist

# item can be None
# return delete item count
def deleteDB(userid, item):
    if userid is not None:
        if item is not None:
            res = mongo.db.frages.delete_one({'userid': userid, 'food':item})
            return res.deleted_count
        else:
            res = mongo.db.frages.delete_many({'userid':userid})
            return res.deleted_count

# if already have same (userid, food) do changeDB
# return type of "change" or "add"
def addDB(userid, food, num, unit, date, dateLeft):
    frage = {'userid':userid, 'food':food, 'num':int(num), 'unit':unit, 'date':date, 'dateLeft':int(dateLeft)}
    #json.dumps(food,encoding='UTF-8',ensure_ascii=False)
    #res = queryDB(userid, food)
    res = queryDB(userid, json.dumps(food,encoding='UTF-8',ensure_ascii=False))
    print len(res)
    if len(res) > 0:
        changeDB(userid, json.dumps(food,encoding='UTF-8',ensure_ascii=False), num, True)
        return "change"
    else:
        mongo.db.frages.insert_one(frage)
        return "add"

# flag = true add, flag = false minus
# if find and change return true else return false
def changeDB(userid, item, num, flag):
    if flag is True:
        res = mongo.db.frages.update_one({'userid': userid}, {'$inc': {'num': num}})
    else:
        num = 0 - num
        res = mongo.db.frages.update_one({'userid': userid}, {'$inc': {'num': num}})
    if res.matched_count is 0:
        return False
    else:
        return True

class InvalidUsage(Exception):
    status_code = 400
 
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
 
@app.errorhandler(InvalidUsage)
def invalid_usage(error):
    response = make_response(error.message)
    response.status_code = error.status_code
    return response

@app.route('/', methods=['post', 'get'])
@app.route('/U-ROBO-1.html', methods=['post','get'])
@app.route('/command/command/command/U-ROBO-1.html', methods=['post','get'])
def timePage():
    #debug
    #date = time.time()
    #localtime = time.localtime(time.time())
    #userid='127.0.0.1'
    #food= '五'.decode('utf-8')
    #num= 3
    #unit='one'
    #dateLeft= 10
    #frage1 = {'userid':userid, 'food':food, 'num':int(num), 'unit':unit, 'date':date, 'dateLeft':int(dateLeft)}
    #frage1Print = json.dumps(frage1,encoding='UTF-8',ensure_ascii=False)
    #print frage1Print
    #frage2 = {'userid':'0.0.0.1', 'food':food, 'num':int(num), 'unit':unit, 'date':date, 'dateLeft':int(dateLeft)}
    #frage3 = {'userid':userid, 'food':'toufu', 'num':int(num), 'unit':unit, 'date':date, 'dateLeft':int(dateLeft)}
    #res = addDB(userid,food,num,unit,date,dateLeft)
    #print res
    #mongo.db.frages.insert_one(frage3)
    #res = queryDB(userid, food)
    #print res

    #res = changeDB(userid, food, 5, True)
    #print res
    return render_template('U-ROBO-1.html')

@app.route('/command', methods=['[post', 'get'])
@app.route('/index', methods=['[post', 'get'])
@app.route('/command/index', methods=['[post', 'get'])
@app.route('/U-ROBO-2.html', methods=['post','get'])
@app.route('/command/command/index', methods=['post', 'get'])
def index():
    # set user cookies
    userid = request.cookies.get('userid')
    if userid is None :
        userid = request.remote_addr
        print 'no cookie'
    resp = make_response(render_template('U-ROBO-2.html'))
    resp.set_cookie('userid', userid)
    return resp

@app.route('/command/request', methods=['get'])
def indexRequire():
    userid = request.cookies.get('userid')
    print userid
    if userid is None :
        print 'no cookie'
        raise InvalidUsage('user doesnt exit', 403)
    else:
        # Query and find items and show
        foodList = queryDB(userid, None)
        print foodList
    resp = make_response(jsonify(foodList))
    return resp

@app.route('/command/router', methods=['post', 'get'])
@app.route('/command/command/router', methods=['post', 'get'])
def commandJump(jump=0):
    global PageCount
    jump = PageCount
    print jump
    if(jump == 7) :
        PageCount = 0
    else :
        PageCount+=1
    if jump is 0:
        return render_template('U-ROBO-3.html')
    if jump is 1:
        return render_template('U-ROBO-3.html')
    if jump is 2:
        return render_template('U-ROBO-4.html')
    if jump is 3:
        return render_template('U-ROBO-4.html')
    if jump is 4:
        return render_template('U-ROBO-5.html')
    if jump is 5:
        return render_template('U-ROBO-3.html')
    if jump is 6:
        return render_template('U-ROBO-3.html')
    if jump is 7:
        return render_template('U-ROBO-3.html')
    return render_template('U-ROBO-2.html')

ALLOWED_EXTENSIONS = set(['wav'])
UPLOAD_FOLDER = './static/audio'

# if the file illegal
def allowed_file(filename):
    # saved in ALLOWED_EXTENSIONS
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/test', methods=['get'])
def testPage():
    return make_response(render_template('test.html'))

@app.route('/command/router/put', methods=['POST'])
def putIn():
    userid = request.cookies.get('userid')
    #wait to be replaced by ('/command/put.html') 
    #resp = make_response(render_template('U-ROBO-4.html'))
    resp = make_response("200")
    resp.status_code=200
    #testdata=request.form
    #testdata.encode('utf-8')
    #print testdata
    #print testdata.len
    if userid is None:
        # no cookies Forbidden
        return redirect(url_for('index'), 403)
#debug
    ticks = time.time()
    food= '苹果'
    num= 12
    unit='one'
    date=ticks
    dateLeft= 4*24
    res = addDB(userid,food,num,unit,date,dateLeft)
    print res
    #if request.method == 'POST':
        #test = request.get_data()["data"]
        #print test
        #with open('test.wav','wb') as f :
            #f.write(testdata)
            #f.close()
        #with wave.open('test.wav', 'rb') as f:

        #print file.len
    #else:
        #raise InvalidUsage('wrong instruction', 400)
    return resp

@app.route('/command/router/get', methods=['POST'])
def getOut():
    userid = request.cookies.get('userid')
    #wait to be replaced by ('/command/put.html') 
    #resp = make_response(render_template('U-ROBO-4.html'))
    resp = make_response("200")
    resp.status_code=200
    #testdata=request.form
    #testdata.encode('utf-8')
    #print testdata
    #print testdata.len
    if userid is None:
        # no cookies Forbidden
        return redirect(url_for('index'), 403)
#debug
    ticks = time.time()
    food= '苹果'
    num= 4
    unit='one'
    date=ticks
    dateLeft= 4*24
    res = changeDB(userid, food,num,False)
    print res
    #if request.method == 'POST':
        #test = request.get_data()["data"]
        #print test
        #with open('test.wav','wb') as f :
            #f.write(testdata)
            #f.close()
        #with wave.open('test.wav', 'rb') as f:

        #print file.len
    #else:
        #raise InvalidUsage('wrong instruction', 400)
    return resp


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route('/command/addFood', methods=['post'])
def addFood():
    userid = request.cookies.get('userid')
    #wait to be replaced by ('/command/change.html') 
    resp = make_response(render_template('U-ROBO-4.html'))
    resp.status_code=200
    if userid is None:
        # no cookies Forbidden
        return redirect(url_for('/'), 403)

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            basepath = os.path.abspath(UPLOAD_FOLDER)
            print os.path.join(basepath, filename)
            file.save(os.path.join(basepath, filename))
            #result = recog(os.path.join(UPLOAD_FOLDER, filename))
            result = {'userid':userid, 'food':'apple', 'num':int(5), 'unit':'', 'date':'', 'dateLeft':int(24)}
            print result
            # split into words

            # save in DB
            changeDB(userid,result['food'],result['num'],True)
            return resp
        else:
            # illegal
            raise InvalidUsage('illegal file input', 403)
    else:
        raise InvalidUsage('wrong instruction', 400)
    return resp

@app.route('/command/getFood', methods=['post'])
def getFood():
    userid = request.cookies.get('userid')
    #wait to be replaced by ('/command/change.html') 
    resp = make_response(render_template('U-ROBO-5.html'))
    resp.status_code=200
    if userid is None:
        # no cookies Forbidden
        return redirect(url_for('/'), 403)

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            basepath = os.path.abspath(UPLOAD_FOLDER)
            print os.path.join(basepath, filename)
            file.save(os.path.join(basepath, filename))
            #result = wordsRecog.main(os.path.join(UPLOAD_FOLDER, filename))
            result = {'userid':userid, 'food':'apple', 'num':int(5), 'unit':'', 'date':'', 'dateLeft':int(24)}
            print result
            # split into words

            # save in DB
            changeDB(userid,result['food'],result['num'], False)
            return resp
        else:
            # illegal
            raise InvalidUsage('illegal file input', 403)
    else:
        raise InvalidUsage('wrong instruction', 400)
    return resp


@app.route('/command/show', methods=['get'])
@app.route('/command/router/show', methods=['get'])
def show():
    userid = request.cookies.get('userid')
    if userid is None :
        print 'no cookie'
        raise InvalidUsage('user doesnt exit', 403)
    else:
        # Query and find items and show
        foodList = queryDB(userid, None)
        print foodList
    resp = make_response(jsonify(foodList))
    return resp



def before_request():
    import glob
    files = glob.glob('static/audio/*')

if __name__ == '__main__':
    
    app.debug = True
    app.run(host='0.0.0.0')
    
