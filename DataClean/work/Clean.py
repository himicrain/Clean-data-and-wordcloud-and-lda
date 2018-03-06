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

#每个json文件保存几个json对象，默认十个,
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

Fields = []
Process_Field = ['comments']

#获取csv的字段名
def get_fields(Dir,file):
    global Fields
    with open(Dir+'/'+file,'r+') as csv_file:
        reader = csv.reader(csv_file)
        line = ';'.join(next(reader))
        if line[:3] == codecs.BOM_UTF8:
            line = line[3:]
        Fields = [x.strip() for x in line.split(';')]


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



def generate_dict(data_list):
    temp = {}

    for i in range(len(Fields)):
        temp[Fields[i]] = data_list[i].strip()
    '''
    temp["messageid"] = data_list[0].strip()
    temp["userid"] =  data_list[1].strip()
    temp["message"] = data_list[2].strip()
    temp["updated_time"] = data_list[3].strip()
    temp["nchar"] = data_list[4].strip()
    '''
    return temp

def clean_file(Dir,file,sign):

    temps = file.split('.')
    clear_file_name = ''.join(temps[:-1])
    count = 0 #记录当前写入json几行了
    file_num = 0 #写了几个json文件了

    with open(Dir+'/'+file,'r+') as csv_file:
        reader = csv.reader(csv_file)
        temp_write_list = []
        csv_file.seek(0, os.SEEK_END)
        length = csv_file.tell()
        csv_file.seek(0)

        print length

        next(reader)

        for line in reader:
            for c in Process_Field:
                index = Fields.index(c)
                clean_line = clean_data(line[index],sign)
                line[index] = clean_line

            line_dict = generate_dict(line)
            count += 1

            if count > COUNT :
                file_num += 1
                clear_file = Dir + '/clean/ ' + clear_file_name + '_clear_'+str(file_num)+'.json'
                f = open(clear_file,"a+")
                json.dump(temp_write_list, f,indent=0)
                temp_write_list = []
                count = 0
                print "generate a clean file ..... , num." + str(file_num)
                f.close()
            else:
                temp_write_list.append(line_dict)

        if temp_write_list != []:
            file_num += 1
            clear_file = Dir + '/clean/ ' + clear_file_name + '_clear_' + str(file_num) + '.json'
            f = open(clear_file, "a+")
            json.dump(temp_write_list, f, indent=0)
            f.close()
            print "generate a clean file ..... , num." + str(file_num)


# 分割符，默认;    注意不能将 - 作为分隔符，
def clean_process(Dir,sign=';'):
    flag = True
    dirs = os.listdir(Dir)
    if not os.path.isdir(Dir + '/clean'):
        os.mkdir(Dir + '/clean')
    else:
        cmd = raw_input('the "clean" dir has existed, do you want to clean this dir ? y for yes, others for no : ')
        if cmd == 'y':
            shutil.rmtree(Dir + '/clean')
            os.mkdir(Dir + '/clean')
        else:
            flag = False
    if flag:
        for file in dirs:
            if os.path.isdir(Dir + '/' + file):
                continue
            get_fields(Dir,file)
            clean_file(Dir, file, sign)
    else:
        print "will not generate clean file"


if '__main__' == __name__:
    clean_process('./csv')