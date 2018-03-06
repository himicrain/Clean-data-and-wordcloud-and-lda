#!/usr/bin/env python3
# coding=utf-8

import csv
import os
import shutil
import json
import time
import datetime
Statistic_All_Data = {}
Fields = []

Statistic_All_Data_By_UpdateTime = {}
Statistic_All_Data_By_SWLTime = {}

#这个里面是时间间隔，比如 ('9/1/2009','12/31/2009') 指 9月1 2009年 到 12 月 31 日 2009年，可以自己添加
#Str_Times = [('9/1/2009','12/31/2009'),('1/1/2010','5/31/2010'),('6/1/2010','12/31/2010'),('1/1/2011','10/31/2011')]

#Update 关键字的日期间隔
Str_Times_Of_Update = [('9/1/2009','12/31/2009'),('1/1/2010','5/31/2010'),('6/1/2010','12/31/2010'),('1/1/2011','10/31/2011')]

# SWL关键字的日期间隔
Str_Times_Of_SWL = [('9/1/2009','12/31/2009'),('1/1/2010','5/31/2010'),('6/1/2010','12/31/2010'),('1/1/2011','10/31/2011')]


Times_Update = []
Times_SWL = []

def classify_by_id_nums(datas):

    global Statistic_All_Data
    userid = datas[0]
    others = datas[1:]

    if userid not in Statistic_All_Data.keys():
        Statistic_All_Data[userid] = [1,[others]]
    else:
        Statistic_All_Data[userid][0] += 1
        Statistic_All_Data[userid][1].append(others)

def get_classify_of_nums(dir,data_dict):
    path = dir + os.sep + 'classified'

    if os.path.isdir(path):
        shutil.rmtree(path)

    os.mkdir(path)

    temp_dict = {}

    for k,v in data_dict.items():


        if v[0] not in temp_dict.keys():
            temp_dict[v[0]] = [(k,v)]
        else:
            temp_dict[v[0]].append((k,v))



    statistic_num = {}


    for k,v in temp_dict.items():

        count = k - 1

        if count == 0:
            continue

        count = count if count <= 5 else 5

        temp_path = path + os.sep + "CSV_" + str(count)+'.csv'

        '''
        统计数量
        '''
        if 'CSV_'+str(count) not in statistic_num:
            statistic_num['CSV_'+str(count)] = 1
        else:
            statistic_num['CSV_'+str(count)] += 1


        f = open(temp_path,'a+')

        w_csv = csv.writer(f)
        w_csv.writerow(Fields)

        for ls in v:
            for l in ls[1][1]:
                temp = [ls[0]]
                temp.extend(l)
                w_csv.writerow(temp)



    temp_path_s = path + os.sep + "CSV_Num_Stastic.json"
    fs = open(temp_path_s, 'a+')
    json.dump(statistic_num,fs)



def str2times(str_time):
    return  datetime.datetime.strptime(str_time,'%m/%d/%Y')

#所有Str_time里的时间转换成秒
def str_2_times():
    global Str_Times_Of_SWL,Str_Times_Of_Update,Times_Update,Times_SWL
    '''
    for t in Str_Times:
    t1 = time.mktime(str2times(t[0]).timetuple())
    t2 = time.mktime(str2times(t[1]).timetuple())
    Times.append((t1,t2))
    '''
    for t in Str_Times_Of_SWL:
        t1 = time.mktime(str2times(t[0]).timetuple())
        t2 = time.mktime(str2times(t[1]).timetuple())
        Times_SWL.append((t1,t2))
    for t in Str_Times_Of_Update:
        t1 = time.mktime(str2times(t[0]).timetuple())
        t2 = time.mktime(str2times(t[1]).timetuple())
        Times_Update.append((t1,t2))


def check_in_tuple_time(t1,tu):

    if t1 >= tu[0] and t1 <= tu[1]:
        return True
    else:
        return False




def classify_by_times(datas,token):
    global Statistic_All_Data_By_SWLTime,Statistic_All_Data_By_UpdateTime
    #位于第一个时间间隔里为1 ， 第二个为2
    flag = -1
    index = Fields.index(token)
    date_time = time.mktime(str2times(datas[index].split()[0]).timetuple())


    if token == 'updated_time':

        for i in range(len(Times_Update)):
            if check_in_tuple_time(date_time, Times_Update[i]) == True:
                flag = i
                break
        if flag == -1:
            return

        if flag not in  Statistic_All_Data_By_UpdateTime.keys():
            Statistic_All_Data_By_UpdateTime[flag] = [datas]
        else:
            Statistic_All_Data_By_UpdateTime[flag].append(datas)

    elif token == 'SWL_taken':

        for i in range(len(Times_SWL)):
            if check_in_tuple_time(date_time, Times_SWL[i]) == True:
                flag = i
                break
        if flag == -1:
            return

        if flag not in Statistic_All_Data_By_SWLTime.keys():
            Statistic_All_Data_By_SWLTime[flag] = [datas]
        else:
            Statistic_All_Data_By_SWLTime[flag].append(datas)

def get_statistic_of_times(dir):
    global Statistic_All_Data_By_SWLTime,Statistic_All_Data_By_UpdateTime,Str_Times_Of_SWL,Str_Times_Of_Update
    path = dir + os.sep + 'classified_times'

    if os.path.isdir(path):
        shutil.rmtree(path)

    os.mkdir(path)

    os.mkdir(path+os.sep+'by_update_time')
    os.mkdir(path+os.sep+'by_SWL_time')


    for k,v in Statistic_All_Data_By_UpdateTime.items():
        name = '-'.join(Str_Times_Of_Update[k][0].split('/')) + '  to  ' + '-'.join(Str_Times_Of_Update[k][1].split('/'))
        file_name = path+os.sep+'by_update_time' + os.sep + name+'.csv'

        f = open(file_name,'a+')
        f_csv = csv.writer(f)
        f_csv.writerow(Fields)

        for l in v:
            f_csv.writerow(l)

    for k,v in Statistic_All_Data_By_SWLTime.items():
        name = '-'.join(Str_Times_Of_SWL[k][0].split('/')) + '  to  ' + '-'.join(Str_Times_Of_SWL[k][1].split('/'))
        file_name = path+os.sep+'by_SWL_time' + os.sep + name+'.csv'

        f = open(file_name,'a+')
        f_csv = csv.writer(f)
        f_csv.writerow(Fields)


        for l in v:
            f_csv.writerow(l)





def load_data(dir,file):
    global Fields

    path = dir + os.sep + file

    f = open(path,'r+')

    f_csv = csv.reader(f)

    Fields = next(f_csv)

    for ls in f_csv:
        classify_by_id_nums(ls)
        classify_by_times(ls,'updated_time')
        classify_by_times(ls,'SWL_taken')
    get_classify_of_nums(dir,Statistic_All_Data)
    get_statistic_of_times(dir)


if __name__ == '__main__':
    #将对应的时间间隔字符串，处理成秒
    str_2_times()

    load_data('./classify_csv','test_data.csv')




