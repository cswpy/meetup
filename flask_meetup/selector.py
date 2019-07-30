import math
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.spatial.distance import cdist
from settings import FIELD_IDX, PRICELIM, REGION, dianPingFields
from voting import dislike, borda, copeland, cuisine
from geometric import geometric_median, minimize_method, weiszfeld_method, getDistance, findField,transform
import redis
import json


class Person(object):
    def __init__(self,dictionary):
        self.cuisine = np.array(dictionary["pref"]).reshape(16,)
        self.price = dictionary["price"]
        self.location = np.array(dictionary["location"]).reshape(2,)


class Selector(object):
    def __init__(self, persons):
        self.persons = [(k,v) for k, v in persons.items()]


    def select(self):
        '''
        This method reads the file uploaded from the Flask application POST request, 
        and performs a selection 
        '''
        VOTER_NUM = len(self.persons)
        FIELD_NUM = 30
        CUISINE_NUM = 16
        cuisinelist = range(16)
        
        personlist = []
        for i in range(VOTER_NUM):
            personlist.append(Person(self.persons[i][1]))

        for Person in personlist:
        #tuple element cannot select object
        #personCuisine = np.array(Person[0]).reshape(16,)
            personCuisine = Person.cuisine
            cuisinelist = np.column_stack((cuisinelist, personCuisine))
        dislikelist=dislike(cuisinelist, 16, VOTER_NUM)
        bordalist=borda(cuisinelist, 5, 16, VOTER_NUM)
        copelandlist=copeland (16, VOTER_NUM, cuisinelist)
        cuisine_selected=cuisine(bordalist, copelandlist, dislikelist)
        
        pricelist = []
        for Person in self.persons:
            pricelist.append(Person.price)
        count0=0
        count1=0
        count2=0
        for i in pricelist:
            if i == 0:
                count0 +=1
            elif i == 1:
                count1 +=1
            else:
                count2 +=1
        price_selected = np.argmax([count0, count1, count2])

        locationlist = np.array(['经度','纬度']).reshape(2,)
        for Person in self.persons:
            personLocation = Person.location
            locationlist = np.column_stack((locationlist, personLocation))
        points = []
        for i in VOTER_NUM:
            points.append(locationlist[:,i])
        medianlist=geometric_median(points, method='weiszfeld', options={})
        location_selected=findField(medianlist)

        df = json.loads()
        #what to specify in loads ()? and how to end the for loop
        dianpingDf = np.array(["OBJECTID","name","location","category","cuisine","cuisine_id",
        "addr","mean_price","rating","longitude","latitude","taste_score","env_score","sevice_score"]).reshape(14,)
        dianping_new = np.array([df['OBJECTID'],df['name'],df['location'],df['category'],df['cuisine'],df['cuisine_id'],
        df['addr'],df['mean_price'],df['rating'],df['longitude'],df['latitude'], df['taste_score'],df['env_score'],df['service_score']]).reshape(14,)
        dianpingDf = np.column_stack((dianpingDf, dianping_new))

        df.dropna(inplace=True)
        df = df[df['category']=='美食']
        fieldid =[]
        fieldid.extend(FIELD_IDX[cuisine_selected[0]])
        fieldid.extend(FIELD_IDX[cuisine_selected[1]])
        fieldid.extend(FIELD_IDX[cuisine_selected[2]])
        fieldid.extend(FIELD_IDX[cuisine_selected[3]])
        fieldid.extend(FIELD_IDX[cuisine_selected[4]])

        regionid = []
        regionid.append(REGION[location_selected[0].astype(int)])
        regionid.append(REGION[location_selected[1].astype(int)])
        regionid.append(REGION[location_selected[2].astype(int)])
        pricelim = PRICELIM[price_selected]

        select_cuisine = df[df['cuisine_id'].isin(fieldid)]
        select_region = select_cuisine[select_cuisine['location'].isin(regionid)]
        select_price = select_region[select_region['mean_price'].astype(int).isin(pricelim)]
        selection = select_price.sort_values(by=['taste_score'],ascending=False)[0:5]
        #what to return for the select_price?
        send = selection.to_json(orient='split')        
        return send