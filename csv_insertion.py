#coding=utf-8

import csv
import redis
import json

r = redis.StrictRedis(host='127.0.0.1', port=6379)

with open('./dianping_database_edited.csv', 'rt') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id = row['OBJECTID']
        data_encoded = json.dumps(row)
        r.set(id,data_encoded)  #将内容写入redis
'''
        ID = row['OBJECTID']
        name = row['名字']
        location = row['地区']
        category = row['大类']
        cuisine = row['菜系14']
        cuisine_id = row['FieldID']
        addr = row['地址']
        mean_price = row['人均价格']
        rating = row['人均价格']
        longitude = row['坐标1']
        latitude = row['坐标2']
        taste_score = row['口味分']
        env_score = row['环境分']
        service_score = row['服务分']
'''