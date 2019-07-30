from flask import Flask, request
import redis
import json
from selector import Selector
import numpy as np
import random

app = Flask(__name__)
REDIS_URL = "redis://:THE-Hack-2019@ec2-52-81-95-240.thehack.org.cn:22/0"

r = redis.Redis(
    host='ec2-52-81-95-240.thehack.org.cn',
    port='6379',
    password='The-Hack-2019'
    )

redis_client = r
room_key_list = list(range(1,100))

@app.route('/preference', methods=['POST'])
def usr_pref():
    pref = str(request.form['pref'])
    price = str(request.form['price'])
    location = str(request.form['location'])
    user_name = str(request.form['user_name'])
    room_key = str(request.form['room_key'])
    if room_key == '':
        random.shuffle(room_key_list)
        room_key = room_key_list.pop()
        room_key = str(room_key)
        #room_key=np.random.sample(room_key_list)
        #room_key_list.remove(room_key)
        person_content = { 'preference': pref, 'price':price, 'location': location, 'user_name' : user_name, 'isOwner' : 'True' }
        redis_client.hmset('username:' + user_name, person_content)
        #print(type(user_name))
        #if redis_client.hmget(room_key):
        #print(type(user_name))
        redis_client.rpush('room_key:' + room_key, user_name)
        return room_key
        
    else:
        #result = redis_client.get('room_key:' + room_key)
        person_content = { 'preference': pref, 'price':price, 'location': location, 'user_name' : user_name, 'isOwner': 'False' }
        redis_client.hmset('username:' + user_name, person_content)
        redis_client.rpush('room_key:' + room_key,user_name)
        return "Success"


@app.route('/confirm', methods=['POST'])

def calculate():
    room_key = str(request.form['room_key'])
    user_name = str(request.form['user_name'])
    if redis.client.hexists(room_key,'outcome')==False:
        if (redis.client.hlen(room_key)!=0) & (redis.client.hget(room_key,'host')['user_name']==user_name):
            user_selector = Selector(redis.client.hgetall(room_key))
            redis.client.hmset(room_key,{'outcome' : user_selector.select()})
    else:
        msg= {'Data Processing, please revisit the page later. Thanks for your patience.'}
        return json.dumps(msg)

@app.route('/hello', methods=['GET'])
def hello():
    return 'hello there'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='4040')



