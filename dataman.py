# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:24:13 2019

@author: user
"""
import numpy as np
import random as rd
import torch as tc

def simplesplit(x,y,fac=10):
    size=len(x)
    z = np.split(rd.sample(range(size),size),[int(size*(1-fac/100))])
    return [x[z[0]],y[z[0]],x[z[1]],y[z[1]]]

def xref(bas,h):
    datrain = []
    datest = []
    htrain = []
    htest = []
    size = len(bas)
    samp = rd.sample(range(size),size)
    x = np.split(samp,np.arange(int(size*0.10),size,int(size*0.10)))
    for i in range(10):
        train = []
        test = []
        for j in range(10):
            if i == j:
                test = x[i]
            else:
                train = np.concatenate((train,x[j]),axis=None)
        xtr = []
        for k in range(len(train)):
            xtr.append(int(train[k]))# for some resson i need to turn the idex to interger again
        datrain.append(bas[xtr])
        datest.append(bas[test])
        htrain.append(h[xtr])
        htest.append(h[test])
        print(i)
    return [datrain,htrain,datest,htest]

def testmodel(mod,actual):
    count = 0     
    for i in range(len(actual)):
        p=np.argmax(mod[i])
        q=actual[i]
        if p == q:
            print(i,')',p,q,'v')
            count = count + 1
        else:
            print(i,')',p,q,'x')
    print(count,'/',len(actual))
    
def acctest(mod,actual):
    count = 0     
    for i in range(len(actual)):
        p=tc.argmax(mod[i])
        q=actual[i]
        if p == q:
            count = count + 1
    l = len(actual)        
    return str(count) + '/'+ str(l)