#!/usr/bin/env python2
# coding=utf-8
'''
function: use clean_process(Dir) , all of the csv files in the dir will be convert to json file which size is decided by the variable COUNT ,
          which means that there will be COUNT(such as 10) json objects in a file

'''

import csv
import json
import shutil
import os
import nltk
import string
import codecs

#每个json文件保存几个json对象，默认十个,如果想要只输出一个文件，那么这个设置成一个很大的数可以了
COUNT = 100000

#第一种分割需要
punctuation = '[\s+\.\!\/_,$%^*(+\")\|]+|[+——()?【】“”！，。？、~@#￥%……&*（）-]+'

#第二种分割需要
punctuations = list(string.letters+"0123456789")

#这里可以添加自己的stopwords
#额外的stopwords
extra_stopWords = ['http','https']

stop_words = nltk.corpus.stopwords.words('english')
stop_words = list(stop_words)

stop_words.extend(extra_stopWords)

def clean_data(data,sign):
    global stop_words

    #第二种分割方法
    for c in data:
        if c=='\'' or c in punctuations:
            continue
        else:
            data = data.replace(c,'-')
    words = data.split('-')

    #第一种分割方法
    #words =[x for x in re.split(punctuation,data) if x]

    for word in words:
        try:
            if word.decode('ascii').lower() in stop_words or word.decode('utf-8').isdigit() :
                words[words.index(word.decode('utf-8'))] = ''
        except:
            words[words.index(word)] = '-'
            continue

    if sign == '-':
        print 'the sign "-" has been used somewhere, please use others signs'

    temp = '-'.join(words)
    words = [x for x in temp.split('-') if x]


    for k,w in enumerate(words):
        words[k] = w.lower()

    return sign.join(words)
