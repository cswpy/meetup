"""
The flask application package.
"""
from flask import Flask, render_template
import redis
from flask_session import Session
#from datetime import datetime
#from main import Selector

app = Flask(__name__)
app.debug= True
db = redis.Redis('127.0.0.1:6379')





if __name__ == '__main__':
    app.run()

