import sys
from sets import Set

def read_device(file_name):
    device_list = [];
    num = 180
    index = -1
    with open(file_name) as f:
        for line in f.readlines():
            list = line.split(" ")
            if (num == 180):
                num = 0
                index += 1
                device_list.append({})
            if (list[0] == '*'):
                num += 1
                continue
            else:
                if (device_list[index].get(list[0]) == None):
                    device_list[index][list[0]] = 1
                else:
                    device_list[index][list[0]] += 1
    return device_list

def get_noise(device_list):
    for dict in device_list:
        for key in dict.keys():
            if (dict[key] < 60):
                del dict[key]
    return device_list

def filter_noise(noise_list):
    result = []
    for i in range(0, 48):
        result.append(Set())
        for key in noise_list[0][i].keys():
            num = 0
            for j in range(1, 5):
                if key in noise_list[j][i]:
                    num += 1
            if num >= 3:
                result[i].add(key)
    return result

def write_clean_file(file_name, result):
    fOutput = open(file_name + 'c.txt' ,"w")
    index = -1
    num = 180
    with open(file_name) as f:
        for line in f.readlines():
            list = line.split(" ")
            if (num == 180):
                num = 0
                index += 1
            if (list[0] == '*'):
                num += 1
                fOutput.write(line)
                continue
            else:
                if (list[0] in result[index]):
                    continue
                else:
                    fOutput.write(line)

def main():
    device_list = []
    noise_list = []
    for i in range(1, 6):
        device_list.append(read_device(sys.argv[i]))
        noise_list.append(get_noise(device_list[i - 1]))
    result = filter_noise(noise_list)
    for i in range(1, 6):
        write_clean_file(sys.argv[i], result)

if __name__ == '__main__':
    main()

