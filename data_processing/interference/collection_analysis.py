POS = ['HH', 'SCOTT', 'WEAN' , 'GATE', 'UC', 'Baker' , 'Porter', 'Doherty', 'DRAMA']
HH_C = [['1'], ['6', '7'], ['9'], ['23'], [], [], [], [], []]
HH_1 = [['5', '12'],['2','4'], ['10'],[],[],['25'],['15'],['18'],[]]
HH_15 = [[],[],[],[],['14', '19', '20', '21'], ['16'],[],['26'],['22']]
HH_2 = [['3', '13'], ['8'],[],[],['24'],[],[],[],[]]
Layers = [HH_C, HH_1, HH_15, HH_2]

def collection_analysis_node(node_list):
    """
        node_list [{}, {}, {}, {}, {}]
    """
    result = []
    count = 0;

    for list in node_list:
        result.append({})
        for key in list.keys():
            pos = getPosition(key)
            if pos in result[count].keys():
                result[count][pos] += node_list[count][key]
            else:
                result[count][pos] = node_list[count][key]

        count += 1

    return result

def collection_analysis_edge(edge_list):

    result = []
    count = 0

    for list in edge_list:
        result.append({})
        for key in list.keys():
            s_arr = key.split(" ")
            pos1 = getPosition(s_arr[0])
            pos2 = getPosition(s_arr[1])
            if (pos1 == pos2):
                continue
            s_temp = pos1 + " " + pos2
            if s_temp in result[count].keys():
                result[count][s_temp] += edge_list[count][key]
            else:
                result[count][s_temp] = edge_list[count][key]
        count += 1

    return result


def getPosition(key):
    x_len = len(Layers)
    y_len = len(POS)
    for i in range(0, x_len):
        for j in range(0, y_len):
            if (key in Layers[i][j]):
                return POS[j] + '_' + str(i)

    return ''


if __name__ == '__main__':
    node_list = [{'1':1,'2':2,'3':3,'4':4,'5':5},{'1':1,'2':2,'3':3,'4':4,'5':5}]
    edge_list = [{'1 1':1,'2 1':2,'3 3':3,'4 7':4,'5 1':5, '5 7':6, '12 7': 7},{'1 1':1,'2 1':2,'3 3':3,'4 7':4,'5 1':5, '5 7':6}]
    node_list = collection_analysis_node(node_list)
    edge_list = collection_analysis_edge(edge_list)
    print node_list
    print edge_list
