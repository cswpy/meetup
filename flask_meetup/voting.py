import pandas as pd
import numpy as np
CUISINE_NUM = 16


#price_majority
def majority_element(pricelist):
        idx, ctr = 0, 1
        
        for i in range(1, len(pricelist)):
            if pricelist[idx] == pricelist[i]:
                ctr += 1
            else:
                ctr -= 1
                if ctr == 0:
                    idx = i
                    ctr = 1
        
        return pricelist[idx]

#Dislike algorithm
def dislike(df, CUSINE_NUM, VOTER_NUM):
    dislikeList = np.zeros(CUSINE_NUM)
    dislike = []
    for i in range(VOTER_NUM):
        for m in range(CUSINE_NUM):
            if df.iloc[m,i+1] == -1:
                dislikeList[m] =-1
    for i in range(len(CUSINE_NUM)):
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
    plurality = np.argmax(firstChoice)
    
    majorityCriterion = False
    for i in bordaList:
        if i == plurality:
            majorityCriterion = True
    if majorityCriterion == False:
        bordaList[OUTPUT-1]=plurality
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

def cusine(bordaList, CUS_BIG, dislike):
    cusList=bordaList

    inList= False
    for i in bordaList:
        if i==CUS_BIG:
            inList=True
    if inList:
        cusList[-1]=CUS_BIG
    for i in dislike:
        if i.isin(cusList):
            cusList2 = cusList.remove(i)
    if cusList2 <3:
        return cusList
    else:
        return cusList2
        
