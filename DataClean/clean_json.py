
# coding=utf-8

import os
import string
import shutil



def clean_data(data,sign):

    flag = True
    if 'RT' in data:
        flag = False

    data_list = []
    data = data.strip()
    datas = data.split('#')[1:]

    has_ = False
    if len(datas) >1 :
        has_ = True
    data_list.extend(datas)

    for l in data_list:
        ls = l.split('http')
        data_list[data_list.index(l)] = ls[0]
    data = '",'.join(data_list)

    return data,flag,has_


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
        has_count = 0
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

                if has_ :
                    has_count += 1

                if write_flag:
                    wr.writelines(temp_str)
                else:
                    RT_count += 1
                temp_str = ''
                continue

            if begin_flag:
                datas = line.strip().split(':')
                if datas[0].strip() == '"text"':
                    cleaned_data,write_flag,has_ = clean_data(datas[1].strip(),sign)
                    temp_str += '\t"text" : "'+cleaned_data+'",\n'
                    #wr.writelines('\t"text" : "'+cleaned_data+'",\n')
                else:
                    temp_str += line



                if datas[0].strip() == '"_id"':
                    count += 1


        wr_count.writelines('{"total_obj_number" : '+str(count) + '}\n')
        wr_count.writelines('{"RT_obj_number" : ' + str(RT_count) + '}\n')
        wr_count.writelines('{"valid_obj_number" : ' + str(count-RT_count) + '}\n')
        wr_count.writelines('{"has_#_sign_number" : ' + str(has_count) + '}\n')

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