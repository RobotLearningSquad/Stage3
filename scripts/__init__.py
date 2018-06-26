#!/usr/bin/env python
from werkzeug.utils import secure_filename
from flask import *
from flask_pymongo import PyMongo
import logging
import os
import time
import bson
from wordsRecog import recog
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

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Session key'
app.config['FLASK_DEBUG'] = 1
app.config.update(
    MONGO_HOST='localhost',
    MONGO_PORT = 27017,
    MONGO_USERNAME='tempo',
    MONGO_PASSWORD='11111111',
    MONGO_DBNAME='frage_DB'
)
mongo = PyMongo(app)


#def addDB(userid, food, num, unit, date, dateLeft):
    #with app.app_context():
        

def quertDB(userid, item):
    if userid is not None:
        if item is not None:
            frage = mongo.db.frages.find_raw_batches({'userid':userid}, {'food':item})
        else:
            frage = mongo.db.frages.find_raw_batches({'userid':userid})
        for food in frage:
            foo = bson.decode_all(food)
            print foo



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
@app.route('/index', methods=['[post', 'get'])
def index():
    #debug
    ticks = time.time()
    localtime = time.localtime(time.time())
    userid='0.0.0.0'
    food= 'apple'
    num= 3
    unit='one'
    date=ticks
    dateLeft= 10
    frage = {'userid':userid, 'food':food, 'num':int(num), 'unit':unit, 'date':date, 'dateLeft':int(dateLeft)}
    print frage
    mongo.db.frages.insert_one(frage)
    
    # set user cookies
    userid = request.cookies.get('userid')
    if userid is None :
        userid = request.remote_addr
        print 'no cookie'
    else:
        # Query and find items and show
        print 'tbc...'
    resp = make_response(render_template('index.html'))
    resp.set_cookie('userid', userid)
    print userid
    return resp

@app.route('/command', methods=['post', 'get'])
def commandJump(jump=0):
    if jump is 0:
        #wait to be replaced by ('/command.html')
        return render_template('')
    if jump is 1:
        return render_template('')
    if jump is 2:
        return render_template('')
    #wait to be replaced by ('/command.html') 
    return render_template('greet.html', name=None)

ALLOWED_EXTENSIONS = set(['wav'])
UPLOAD_FOLDER = './static/audio'

# if the file illegal
def allowed_file(filename):
    # saved in ALLOWED_EXTENSIONS
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/command/put', methods=['post'])
def putIn():
    userid = request.cookies.get('userid')
    #wait to be replaced by ('/command/put.html') 
    resp = make_response(render_template('upload.html'))
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
            result = recog(os.path.join(UPLOAD_FOLDER, filename))
            print result
            # split into words

            # save in DB

            return resp
        else:    
            # illegal
            raise InvalidUsage('illegal file input', 403)
    else:
        raise InvalidUsage('wrong instruction', 400)
    return resp

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route('/command/change', methods=['post'])
def changeIn():
    userid = request.cookies.get('userid')
    #wait to be replaced by ('/command/change.html') 
    resp = make_response(render_template('upload.html'))
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
            result = recog(os.path.join(UPLOAD_FOLDER, filename))
            print result
            # split into words

            # save in DB

            return resp
        else:
            # illegal
            raise InvalidUsage('illegal file input', 403)
    else:
        raise InvalidUsage('wrong instruction', 400)
    return resp

@app.route('/command/show', methods=['get'])
def show():
    userid = request.cookies.get('userid')
    #wait to be replaced by ('/command/show.html') 
    resp = make_response(render_template('upload.html'))
    resp.status_code = 200
    if userid is None:
        # no cookies Forbidden
        return redirect(url_for('/'), 403)
    
    # set DB items into response
    return resp



def before_request():
    import glob
    files = glob.glob('static/audio/*')

if __name__ == '__main__':
    
    app.debug = True
    app.run(host='0.0.0.0')
    