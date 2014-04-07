from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import time

app = Flask(__name__)

currentUser = ''

@app.route('/')
def mainIndex():
    client = MongoClient()
    db = client.lojong
    result = []
    for slogan in db.slogans.find():
      result.append(slogan)
      
    #### demo section -- delete when modifying code
    
    # get weekday
    day = time.strftime("%A")
    # get browser 
    user_agent = request.user_agent.string
    ## construct json like entry
    logPost = {"day": day, "user_agent": user_agent}
    log = client.log
    log.visitors.insert(logPost)
    ### demo section end
    
    return render_template('index.html', results=result, selectedMenu='Home')
    
@app.route('/insert')
def insert():
    client = MongoClient()
    db = client.lojong
    print db.slogans.find_one()
    result = []
    for slogan in db.slogans.find():
      result.append(slogan)
    return render_template('insert.html', selectedMenu='Insert')
    
    
@app.route('/log')
def log():
    client = MongoClient()
    db = client.log
    result = []
    day = time.strftime("%A")
    for entry in db.visitors.find({"day": day}):
      result.append(entry)
    return render_template('log.html', results=result, selectedMenu='Log')
     

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=3000)
