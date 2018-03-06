
# coding=utf-8

import os
import string
import shutil
import codecs
import csv
#第二种分割需要
punctuations = list(string.letters+"0123456789")

Fields = []
Statistic_Id_With_Rating = {}
Statistic_Avg_With_Rating = {}

def split_comment(data):
    #第二种分割方法
    for c in data:
        if c=='\'' or c in punctuations:
            continue
        else:
            data = data.replace(c,'-')
    words = data.split('-')

    return len(words)

def process_comments(count,comments):

    sum = 0
    for l in comments:
        num = split_comment(l)
        sum += num

    avg = sum/float(count)

    return avg


def statistic_data(avg,detials, comments):
    global Statistic_Id_With_Rating
    global Statistic_Avg_With_Rating
    rating = detials[2]

    if rating not in Statistic_Id_With_Rating.keys():
        Statistic_Id_With_Rating[rating] = [detials]
    else:
        Statistic_Id_With_Rating[rating].append(detials)



    if rating not in  Statistic_Avg_With_Rating.keys():
        Statistic_Avg_With_Rating[rating] = [avg]
    else:
        Statistic_Avg_With_Rating[rating].append(avg)



def statistic_1(dict_data,Dir):
    #第一个的统计

    path = Dir+os.sep+'statistic'+os.sep+'statistic_1.csv'

    if os.path.isfile(path):
        os.remove(path)

    f = open(path,'wb')

    fields = ['overall rating','Total numbers of roo ID']
    fields.extend(Fields[:2])
    fields.extend(Fields[3:-1])
    writer = csv.writer(f)
    writer.writerow(fields)

    flag = True
    for k,v in dict_data.items():
        for l in v:
            temp = ['','']
            temp.extend(l[:2])
            temp.extend(l[3:])
            if flag == True:
                temp[0] = k
                temp[1] = str(len(v))
                flag = False
            writer.writerow(temp)

        flag = True

def statistic_2(avg,detial, comments,Dir):


    path = Dir+os.sep+'statistic'+os.sep+'statistic_2.csv'
    flag = False
    if os.path.isfile(path):
        flag = True
    f = open(path,'a+')
    writer = csv.writer(f)

    if flag == False:
        writer.writerow(['room ID','Overall rating','Avg. length'])

    writer.writerow([detial[0],detial[2],str(avg)])
    f.close()

def statistic_3(Dir):
    path = Dir+os.sep+'statistic'+os.sep+'statistic_3.csv'
    if os.path.isfile(path):
        os.remove(path)

    f = open(path,'wb')
    writer = csv.writer(f)

    writer.writerow(['Overall rating','Avg.length'])

    for k,v in Statistic_Avg_With_Rating.items():
        sum = 0
        for a in v:
            sum += int(a)

        avg = sum/len(v)

        writer.writerow([k,str(avg)])

    f.close()





def load_data(Dir,file):
    global Fields
    if not os.path.isdir(Dir+os.sep+'statistic'):
        os.mkdir(Dir+os.sep+'statistic')

    if os.path.isfile(Dir+os.sep+'statistic'+os.sep+'statistic_2.csv'):
        os.remove(Dir+os.sep+'statistic'+os.sep+'statistic_2.csv')


    f = open(Dir+os.sep+file)

    reader = csv.reader(f)
    Fields = next(reader)
    if Fields[0][:3] == codecs.BOM_UTF8:
        Fields[0] = Fields[0][3:]

    usefull = True
    Count = 0
    detial = []
    comments = []
    for line in reader:
        if line[1] != '':
            if comments != []:
                avg = process_comments(int(detial[1]), comments)
                statistic_data(avg,detial,comments)
                statistic_2(avg,detial,comments,Dir)
            comments = []
            if line[2] == '':
                usefull = False
            else:
                usefull = True
            Count = int(line[1])
            detial = line[:-1]
        if Count != 0:
            if usefull == True:
                comments.append(line[-1])
            Count -= 1

    if comments != []:
        avg = process_comments(int(detial[1]), comments)
        statistic_data(avg,detial,comments)
        statistic_2(avg,detial, comments, Dir)

    statistic_1(Statistic_Id_With_Rating,Dir)
    statistic_3(Dir)

if "__main__" == __name__:

    Dir = '.' # 当前目录下
    data_file = 'new_data.csv'
    load_data(Dir,data_file)
