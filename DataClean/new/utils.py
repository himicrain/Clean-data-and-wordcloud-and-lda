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

Sign = ';'

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

            keyword = 'message' #处理的列



            print (Dir+os.sep+file)
            reader = csv.reader(f)
            fields = next(reader)
            index = fields.index(keyword)


            for l in reader:
                line = Clean.clean_data(l[-1], Sign)
                if line.strip() != '':
                    w.writelines(line+'\n')
    return str_path+'str.txt'



