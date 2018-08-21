
# coding: utf-8
from pathlib2 import Path
from datetime import datetime
from dateutil import parser

"""
    BLE Sesning data recovery.
    author: Zhengkai Zhang
"""

node = [1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,18,19,20,21,22,23,24,25,26]

def recover(date, path):
    """
        args:
        data: the data of the data
        path: path data_collection folded
    """
    for n in node:
        file_list = []
        # generate path
        if (n > 9):
            ro = path + '/node' + str(n) + '/data/' + 'n' + str(n) + '_' + date + '_'
        else:
            ro = path + '/node0' + str(n) + '/data/' + 'n' + str(n) + '_' + date + '_'

        my_file = ro + '0.txt'
        count = 1
        # add all of the files in one dat into a list
        while (Path(my_file).is_file()):
            file_list.append(my_file)
            my_file = ro + str(count) + '.txt'
            count += 1

        # Start data recovering process
        if (len(file_list) == 0):
            print ('File Error: Node ' + str(n) + ' in ' + date + '!')
            print ('****Data Loss****\n')
            continue

        if (len(file_list) == 1):
            continue
        print ('File Error: Node ' + str(n) + ' in ' + date + '!')
        print ('Recovering...')
        recover_helper(file_list, ro)
        print ('Finishing Data Recovering!\n')

def recover_helper(file_list, path):
    """
        args:
        file_list: the files list
        path: the path of the files folder
    """
    ro = path + 'r.txt'
    # for the end point analysis
    end_of_day = parser.parse('23:59:59.9999')
    start_of_day = parser.parse('00:00:00.0000')
    # prev shows the datetime shows before
    prev = parser.parse('00:00:00.00000')
    # datetime right now
    now = parser.parse('00:00:00.00000')
    with open(ro, 'w') as new_file:
        # iterate files in the list
        for file_rc in file_list:
            with open(file_rc) as f:
                #iterate the lines in this file
                for line in f.readlines():
                    line_split = line.split(" ")
                    # data like this: * 
                    # break
                    if (len(line_split) < 2):
                        break
                    # time frame data
                    if (line_split[0] == '*'):
                        # time frame data not complete like: * date time 
                        # break not get into next file
                        if (len(line_split) != 4):
                            break
                        now = parser.parse(line_split[2])
                        # abnormal situation 
                        if (now < prev):
                            continue
                        dt = now - prev
                        # normal siutation
                        if (dt.seconds < 30):
                            new_file.write(line)
                            prev = now
                            continue
                        # add fake data into data set
                        for i in range(dt.seconds / 10):
                            new_file.write("* **** **** ****\n")
                        new_file.write(line)
                        # switch
                        prev = now
                    else:
                        if (now < prev):
                            continue
                        new_file.write(line)
        # get into the new day already
        if (now > start_of_day):
            return
        # old day not complete
        if (now < end_of_day):
            dt = end_of_day - now
            for i in range(dt.seconds / 10):
               new_file.write("* **** **** ****\n")

if __name__ == '__main__':
    recover('2018-07-16', '/Users/zhengkaizhang/Desktop/data_processing/data_collection')

