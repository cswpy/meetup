import sys
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.spatial.distance import cdist
import math

FIELD_IDX = [['g110','g221','g208','g32733','g3027'],['g250','g206','g2774','g203'],
            ['g229','g227','g115'],['g205','g207'],['g225','g508','g219'],
            ['g3243'],['g224','g226'],['g198','g101','g199','g201','g202','g212','g211','g200'],
            ['g1821','g1881','g213','g1819'],['g251'],['g114'],['g104','g4467'],
            ['g116','g233','g232','g231','g254'],['g20038'],['g109'],
            ['g111'],['g133'],['g132'],['g242','g132','g117'],['g134'],
            ['g217','g112','g223','g210','g24340']]
PRICELIM = [list(range(100)), list(range(100, 200)), list(range(200, 100000))]
REGION = ['七宝','上海影城/新华路','中山公园','临平路/和平公园','人民广场',
         '八佰伴','动物园/虹桥机场','南京东路','南京西路','外滩','徐家汇','打浦桥',
         '新天地','曲阳地区','海宁路/七浦路','淮海路','火车站','老西门','肇嘉浜路沿线',
         '莘庄','虹桥','衡山路','长寿路','静安寺','音乐学院','张江','四川北路','金桥',
         '长风公园','世纪公园']
dianPingFields = np.matrix([['七宝', [31.157650, 121.351240]],['上海影城/新华路',[31.202300, 121.429760]],
                          ['中山公园',[31.218457, 121.418137]],['临平路/和平公园',[31.270800, 121.503430]],
                          ['人民广场',[31.232708, 121.475537]],['八佰伴',[31.228990, 121.517570]],
                          ['动物园/虹桥机场',[31.196680, 121.337600]],['南京东路',[31.234687, 121.479834]],
                          ['南京西路',[31.228100, 121.459442]],['外滩',[31.231820, 121.493706]],
                          ['徐家汇',[31.192800, 121.440770]],['打浦桥',[31.206287, 121.468965]],
                          ['新天地',[31.219860, 121.476300]],['曲阳地区',[31.279330, 121.491380]],
                          ['海宁路/七浦路',[31.245310, 121.478740]],['淮海路',[31.214120,121.452060]],
                          ['火车站',[31.249601,121.455704]],['老西门',[31.219060,121.483686]],
                          ['肇嘉浜路沿线',[31.199465,121.450231]],['莘庄',[31.111226,121.385377]],
                          ['虹桥',[31.196770,121.152740]],['衡山路',[31.204983,121.446727]],
                          ['长寿路',[31.240082,121.437954]],['静安寺',[31.223440,121.445300]],
                          ['音乐学院',[31.213310,121.454320]],['张江',[31.179220, 121.591563]],
                           ['四川北路',[31.252025, 121.484315]],['金桥',[31.260884, 121.611497]],
                           ['长风公园',[31.225160, 121.400910]],['世纪公园',[31.216317, 121.552864]]])

#need constant variable: VOTER_NUM
from voting import dislike, borda, copeland, cusine, majority_element
from geometric import geometric_median, minimize_method, weiszfeld_method, getDistance, findField,transform

CUSINE_NUM = 16
FIELD_NUM = 30

class Selector:
    def __init__(self):
        # load database, cuisine_preference, VOTER_NUM, points, price
        self.userdata = pd.read_csv('sample_vote.csv')
        self.database = pd.read_csv('dianping_database.csv')
        #data pre-processing
        VOTER_NUM=self.userdata.shape()[1] -1
        
        pricelist=self.userdata[18]
        self.price=majority_element(pricelist)
        locationlist=self.userdata[19:20]
        points=transform(locationlist)
        medianlist=geometric_median(points, method='weiszfeld', options={})
        self.regionlist=findField(medianlist)

        cusine_preference = self.userdata[0:17]
        dislikelist=dislike(cusine_preference, CUSINE_NUM, VOTER_NUM)
        bordalist=borda(cusine_preference, 3, CUSINE_NUM, VOTER_NUM)
        copelandlist=copeland (CUSINE_NUM, VOTER_NUM, cusine_preference)
        self.cusinelist=cusine(bordalist, copelandlist, dislikelist)
        

    def select(self):
        df=self.database
        fieldid =[]
        fieldid.extend(FIELD_IDX[self.cusinelist[0]])
        fieldid.extend(FIELD_IDX[self.cusinelist[1]])
        fieldid.extend(FIELD_IDX[self.cusinelist[2]])

        select_cuisine = df[df['FieldID'].isin(fieldid)]
        select_region = select_cuisine[select_cuisine['地区']==REGION[int(self.regionlist[0])]]
        if len(select_region) ==0:
            select_region2 = df[df['地区']==REGION[int(self.regionlist[1])]]
            if len(select_region2) ==0:
                print("双地区筛选失败，返回菜系一")
                return select_region.sort_values(by=['综合评分'],ascending=False)[0:3]
            elif len(select_region2)<=3:
                print ("返回次选地区菜系")
                return select_region2.sort_values(by=['综合评分'],ascending=False)
            else:
                print ("返回次选地区前三菜系")
                return select_region2.sort_values(by=['综合评分'],ascending=False)[0:3]
        elif len(select_region) <=3:
            print ("返回首选地区菜系")
            return select_region.sort_values(by=['综合评分'],ascending=False)
        else:
            pricelim = PRICELIM[self.price]
            select_price = select_region[select_region['人均价格'].isin(pricelim)]
            if len(select_price) ==0:
                print ("首选价格筛选失败，返回地区菜系筛选结果")
                return select_region.sort_values(by=['综合评分'],ascending=False)[0:3]
            elif len(select_price) <=3:
                print ("返回地区菜系价格前三菜系")
                return select_price.sort_values(by=['综合评分'],ascending=False)
            else:
                print ("返回最优选择")
                return select_price.sort_values(by=['综合评分'],ascending=False)[0:3]
        #price 0-100以下， 1-100至200， 2-200以上
