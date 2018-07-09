from sets import Set
from noise_removal import get_static_dict_all_day
from get_device_dict import device_to_dict
import sys

node = [3,5,6,9,11,12,13]

def get_transistion_data(input_date):
    count = 0
    for node_num in node:
        file_name = 'n' + str(node_num) + '_' + input_date + '_0.txt'
        fOutput = fOutput = open('n' + str(node_num) + '_' + input_date + '_t.txt', "w")
        static_set = get_static_dict_all_day(device_to_dict(file_name))
        with open(file_name) as f:
            set_old_1 = Set()
            set_old_2 = Set()
            set_new = Set()
            for line in f.readlines():
                list = line.split(" ")
                temp = 0
                if (list[0] == '*'):
                    set_old_2 = set_old_1
                    set_old_1 = set_new
                    set_new = Set()
                    fOutput.write(line)
                    continue
                else:
                    if list[0] in static_set:
                        continue
                    set_new.add(list[0])
                    if (list[0] in set_old_1) | (list[0] in set_old_2):
                        continue
                    else:
                        fOutput.write(line)
            fOutput.close()

def main():
    get_transistion_data(sys.argv[1])

if __name__ == '__main__':
    main()
