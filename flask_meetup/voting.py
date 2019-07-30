import pandas as pd
import numpy as np
CUISINE_NUM = 16


#Dislike algorithm
def dislike(df, CUSINE_NUM, VOTER_NUM):
    dislikeList = np.zeros(CUSINE_NUM)
    dislike = []
    for i in range(VOTER_NUM):
        for m in range(CUSINE_NUM):
            if df.iloc[m,i+1] == -1:
                dislikeList[m] =-1
    for i in range(CUSINE_NUM):
        if dislikeList[i]==-1:
            dislike.append(i)
    return dislike

#Borda Count Algorithm
def borda (df, OUTPUT, CUSINE_NUM, VOTER_NUM):
    count = df.sum(axis=1)
    count_sorted = count.sort_values(ascending=False)
    bordaList = count_sorted[0:OUTPUT].index

    firstChoice =np.zeros(CUSINE_NUM)
    for m in range(CUSINE_NUM):
        for i in range(VOTER_NUM):
            if df.iloc[m,i+1] == 2:
                firstChoice[m] += 1
    return bordaList

#Copeland's Method Algorithm
def copeland (CUSINE_NUM, VOTER_NUM, df):
    CUS_BIG = 0
    CUS_SMALL = 1
    for unknown in range(1,CUSINE_NUM):
        CUS_SMALL=unknown
        VOTE1=0
        VOTE2=0
        for i in range(VOTER_NUM-1):
            if df.iloc[CUS_BIG, i+1]>df.iloc[CUS_SMALL, i+1]:
                VOTE1 +=1
            elif df.iloc[CUS_BIG,i+1] == df.iloc[CUS_SMALL, i+1]:
                VOTE1 +=0.5
                VOTE2 +=0.5
            else:
                VOTE2 +=1
        if VOTE1 <= VOTE2:
            CUS_BIG = CUS_SMALL
            CUS_SMALL = unknown
    return CUS_BIG

def cuisine(bordaList, CUS_BIG, dislike):
    cusList=bordaList
    print(cusList, CUS_BIG)

    inList= False
    for i in bordaList:
        if i==CUS_BIG:
            inList=True
    if inList:
        pass
    else:
        cusList[-1]=CUS_BIG
    
    cusList=pd.Series(cusList)
    isDislike=[False,False,False,False,False]
    for i in range(5):
        for m in cusList:
            if i==m:
                isDislike[i]=True
    cusList2 = cusList[isDislike]
    if len(cusList2) <3:
        return cusList
    else:
        return cusList2
        
