#!/usr/bin/env python2
# coding=utf-8
'''
function : use the function get_word_frequency_N(N) to get the top N  words frequency

'''
import Clean
import os
from collections import Counter
import time
import csv
start = time.time()
Sign = ';'

Process_Fields = ['comments']
Fields = []
#对每个json对象然后词频统计
def statistic_word_frequency_from_json(json_objs):
    global Sign

    frequency = {}
    for obj in json_objs:
        str_data = obj['comments']
        datas = str_data.split(Sign)
        print '-------', time.time() - start
        frequency = dict(Counter(datas)+Counter(frequency))
    return frequency
#'deded'
#对每个字符串进行词频统计
def statistic_word_frequency_from_str(str_data):
    global Sign
    datas = str_data.split(Sign)
    frequency = Counter(datas)
    return frequency

#对每个文件处理
def process_file(path):
    with open(path,'r+') as f:
        #json_objs = json.load(f,encoding='utf-8')
        #frequency =  statistic_word_frequency_json(json_objs)
        print path
        frequency = Counter()
        reader = csv.reader(f)
        next(reader)
        for l in reader:
            line = Clean.clean_data(l[-1],Sign)
            frequency = statistic_word_frequency_from_str(line)+frequency
        return frequency

#处理Dir下的所有文件进行
def process_files(Dir):
    global start
    Word_Frequency = Counter()
    dirs = os.listdir(Dir)
    for file in dirs:
        if os.path.isdir(Dir+os.sep+file):
            continue
        temp_Counter = process_file(Dir+os.sep+file)
        Word_Frequency = Word_Frequency+temp_Counter
    return Word_Frequency

#获取词频最高的N个词
def get_word_frequency_N(N):
    #清理文件，同时生成./csv/clean文件夹，该文件夹下是处理好的数据
    global start
    #clean.clean_process('./csv')
    word_frequency = process_files('./csv').most_common(N)

    return word_frequency


#生成csv对应的json文件
def generate_json_file():
    Clean.clean_process('./csv')

#将csv中的comments字段的数据提取出来，处理后写入一个新文件里，str.txt。
def generate_str_file(Dir,file):
    str_path = Dir+os.sep+'clean/'
    if not os.path.isdir(str_path):
        os.mkdir(str_path)
    if os.path.isfile(str_path+'str.txt'):
        cmd = raw_input("生成的文件已经存在，是否覆盖 y/n : ")
        if cmd == 'y' :
            os.remove(str_path+'str.txt')
        else:
            return str_path+'str.txt'

    with open(Dir+os.sep+file,'r+') as f:
        with open(str_path+'str.txt','a+') as w:

            #json_objs = json.load(f,encoding='utf-8')
            #frequency =  statistic_word_frequency_json(json_objs)
            print (Dir+os.sep+file)
            reader = csv.reader(f)
            next(reader)
            for l in reader:
                line = Clean.clean_data(l[-1], Sign)
                if line.strip() != '':
                    w.writelines(line+'\n')
    return str_path+'str.txt'

if "__main__" == __name__:
    n_words = get_word_frequency_N(50)
    for word in n_words:
        print word
    print 'time 2 : ', time.time() - start


