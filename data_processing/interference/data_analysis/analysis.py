from matplotlib.ticker import MaxNLocator
from matplotlib import pyplot as plt
from collections import namedtuple
import numpy as np

def connectivity_analysis(edge_list, date):
    length = len(edge_list)
    key_list = []
    num_list = []
    x = range(0, 52)
    for i in range(0, length):
        temp = -1
        key_temp = ""
        for key in edge_list[i].keys():
            if (edge_list[i][key] > i):
                temp = edge_list[i][key]
                key_temp = key
        key_list.append(key)
        num_list.append(temp)

    fig, ax = plt.subplots()
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor':'0.3'}
    rects = ax.bar(x, num_list, bar_width, alpha=opacity, error_kw=error_config)

    ax.set_ylabel('number of connectivity')
    ax.set_xlabel('Time (15min)')

    for rect, key in zip(rects, key_list):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height + 5, key, ha='center', va='bottom', rotation='vertical')

    plt.savefig(date + 'connectivity.png', bbox_inches='tight')






