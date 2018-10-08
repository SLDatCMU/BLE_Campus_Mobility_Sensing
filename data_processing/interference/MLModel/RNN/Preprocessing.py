
# coding: utf-8

# In[57]:


import datetime
import Recover
import filter_data
import numpy as np


# ### Data Recovery  {1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13} 11

# In[60]:

node = [1,2,3,4,5,6,7,8,9,12,13]
start = datetime.datetime.strptime("2018-08-27", "%Y-%m-%d")
end = datetime.datetime.strptime("2018-10-03", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
#date_generated = ['2018-10-04']

def getdate():
    start = datetime.datetime.strptime("2018-08-27", "%Y-%m-%d")
    end = datetime.datetime.strptime("2018-10-03", "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    return date_generated


def data_single_day(date, node):
    path = '/Users/zhengkaizhang/Desktop/data_processing/graph/' + date + '/'
    population = []
    for n in node:
        single = []
        f_path = path + 'n' + str(n) + '_' + date + '_c.txt'
        with open(f_path) as f:
            count = 0
            pop = 0
            for line in f.readlines():
                arr = line.split(' ')
                if arr[0] == '*':
                    count += 1
                    if count < 360:
                        continue
                    else:
                        single.append(int(pop / count))
                        count = 0
                        pop = 0
                else:
                    pop += 1

            single.append(pop / count)
        population.append(np.array(single))

    np.save('./data/' + date + '.npy', population)

def all_data(date_list, node):
    for date in date_list:
        print(str(date)[:10])
        data_single_day(str(date)[:10], node)
    print("Finish!")

def concatenate(date_list, node):
    data = []
    for date in date_list:
        if str(date)[:10] == "2018-09-28":
            continue
        if date.weekday() >= 5:
            continue
        tmp = np.load("./data/" + str(date)[:10] + '.npy')
        data.append(tmp.reshape(24, len(node)))
    return np.array(data)


for date in date_generated:
    Recover.re(str(date)[0:10])

for date in date_generated:
    filter_data.main(str(date)[0:10])

all_data(date_list=['2018-10-04'], node=node)

#data = concatenate(date_list=date_generated, node=node)

