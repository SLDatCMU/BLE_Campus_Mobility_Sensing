node_scott = {'2':0,'4':0, '7':0, '8':0, '10':0} # 24
node_HH = {'1':0,'3':0, '5':0, '12':0, '13':0} # 25

def collection_analysis_node(node_list):
    for list in node_list:
        for key in node_scott.keys():
            if (key in list):
                temp = list[key]
                del list[key]
                if ('24' in list):
                    list['24'] += temp
                else:
                    list['24'] = temp
        for key in node_HH.keys():
            if (key in list):
                temp = list[key]
                del list[key]
                if '25' in list:
                    list['25'] += temp
                else:
                    list['25'] = temp
    return node_list

def collection_analysis_edge(edge_list):
    for list in edge_list:
        for key in list.keys():
            changed = False
            string_array = key.split(" ");
            if (string_array[0] in node_scott) & (string_array[1] in node_scott):
                del list[key]
                continue
            if (string_array[0] in node_HH) & (string_array[1] in node_HH):
                del list[key]
                continue
            for i in range(0, 2):
                if string_array[i] in node_scott.keys():
                    changed = True
                    string_array[i] = '24'
                if (string_array[i] in node_HH.keys()):
                    changed = True
                    string_array[i] = '25'
            if (changed):
                temp = list[key]
                del list[key]
                if string_array[0] + " " + string_array[1] in list.keys():
                    list[string_array[0] + " " + string_array[1]] += temp
                else:
                    list[string_array[0] + " " + string_array[1]] = temp
    return edge_list


if __name__ == '__main__':
    node_list = [{'1':1,'2':2,'3':3,'4':4,'5':5},{'1':1,'2':2,'3':3,'4':4,'5':5}]
    edge_list = [{'1 1':1,'2 1':2,'3 3':3,'4 7':4,'5 1':5, '5 7':6, '12 7': 7},{'1 1':1,'2 1':2,'3 3':3,'4 7':4,'5 1':5, '5 7':6}]
    node_list = collection_analysis_node(node_list)
    edge_list = collection_analysis_edge(edge_list)
    print node_list
    print edge_list
