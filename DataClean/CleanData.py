
# coding=utf-8

import os
import string
import nltk
import shutil

#第一种分割需要
punctuation = '[\s+\.\!\/_,$%^*(+\")\|]+|[+——()?【】“”！，。？、~@#￥%……&*（）-]+'

#第二种分割需要
punctuations = list(string.letters+"0123456789")

#额外的stopwords
extra_stopWords = ['http','https']


def clean_data(data,sign):

    #第二种分割方法
    for c in data:
        if c=='\'' or c in punctuations:
            continue
        else:
            data = data.replace(c,'-')
    words = data.split('-')


    #第一种分割方法
    #words =[x for x in re.split(punctuation,data) if x]
    stop_words = nltk.corpus.stopwords.words('english')
    stop_words = list(stop_words)

    stop_words.extend(extra_stopWords)




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

    flag = True
    if 'RT' in words:
        flag = False

    for k,w in enumerate(words):
        words[k] = w.lower()




    return sign.join(words),flag


def clean_file(Dir,file,sign):
    temps = file.split('.')
    clear_file = ''.join(temps[:-1])
    count_file = Dir + 'clean/'+clear_file + '_count.' + temps[-1]
    clear_file = Dir + 'clean/'+clear_file + '_clear.'+temps[-1]

    wr = open(clear_file,'a+')
    wr_count = open(count_file, 'a+')

    print  Dir+file+'      cleaning....'


    temp_str = ''
    begin_flag = False
    end_flag = False
    write_flag = True


    with open(Dir+file) as json_file:
        count = 0
        RT_count = 0
        for line in json_file:

            if line.strip() == '{':
                begin_flag = True
                temp_str += '{\n'
                end_flag = False
                continue
            if line.strip() == '}':
                begin_flag = False
                temp_str += '}\n'
                end_flag = True

            if end_flag:

                if write_flag:
                    wr.writelines(temp_str)
                else:
                    RT_count += 1
                temp_str = ''
                continue

            if begin_flag:
                datas = line.strip().split(':')
                if datas[0].strip() == '"text"':
                    cleaned_data,write_flag = clean_data(datas[1].strip(),sign)
                    temp_str += '\t"text" : "'+cleaned_data+'",\n'
                    #wr.writelines('\t"text" : "'+cleaned_data+'",\n')
                else:
                    temp_str += line
                    #wr.writelines(line)


                if datas[0].strip() == '"_id"':
                    count += 1


        wr_count.writelines('{"total_obj_number" : '+str(count) + '}\n')
        wr_count.writelines('{"RT_obj_number" : ' + str(RT_count) + '}\n')
        wr_count.writelines('{"valid_obj_number" : ' + str(count-RT_count) + '}\n')

    print  Dir + file + '      clean over....'

def main():

    Dir = './json/'
    dirs = os.listdir(Dir)
    #分割符，默认;    注意不能将 - 作为分隔符，
    sign = ';'

    if not os.path.isdir(Dir+'clean'):
        os.mkdir(Dir+'clean')
    else:
        cmd = raw_input('the "clean" dir has existed, do you want to clean this dir ? y for yes, others for no : ')
        if cmd == 'y':
            shutil.rmtree(Dir+'clean')
            os.mkdir(Dir + 'clean')



    for file in dirs:
        if os.path.isdir(Dir+file):
            continue

        clean_file(Dir,file,sign)

if '__main__' == __name__:

    main()