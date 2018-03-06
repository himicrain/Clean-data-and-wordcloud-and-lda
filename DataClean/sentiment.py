#!/usr/bin/env python2
# coding=utf-8

from textblob import TextBlob
import os
import csv
from matplotlib import pyplot as plt
import time

Statistic = {'Nutral': 0, 'Positive': 0, 'Negative': 0}

def statistic_sentiment(Dir,file):
    global Statistic
    i = 0
    with open(Dir+os.sep+file,'r+') as f:
        reader = csv.reader(f)
        next(reader)
        for datas in reader:
            line = datas[-1].strip()
            line = line.decode('utf-8')
            p = TextBlob(line)
            pro,sub = p.sentiment
            if pro < 0 :
                Statistic['Negative'] += 1
            elif pro == 0:
                Statistic['Nutral'] += 1
            else:
                Statistic['Positive'] += 1
            print i, pro
            i += 1



def draw(Dir,file):
    start = time.time()

    statistic_sentiment(Dir, file)

    plt.figure(figsize=(6,9))
    #print Statistic.items()
    labels = []
    sizes = []
    for k,i in Statistic.items():
        labels.append(k)
        sizes.append(i)
    sum  = 0
    for x in sizes:
        sum += x
    sizes = [float(x)/sum for x in sizes]
    colors = ['red','yellowgreen','lightskyblue']

    explode = (0,0,0)
    patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors,labeldistance=1.1,autopct='%3.1f%%',shadow=False,
                                    startangle=90,pctdistance=0.8)

    for t in l_text:
        t.set_size = (30)
    for t in p_text:
        t.set_size = (20)

    print 'use time : ', int(time.time() - start)
    plt.axis('equal')
    plt.legend()
    plt.show()


if "__main__" == __name__:
    Dir = './csv'
    file = 'data new version.csv'
    draw(Dir,file)

    print Statistic
    print "over "