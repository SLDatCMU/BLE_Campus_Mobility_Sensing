import matplotlib.pyplot as plt
import numpy as np
import scipy
import sys
from time_duration import count_population, count_population_helper
'''
   Distance_calculation of trajectory
   Author: Peng Chen
'''

'''
One-way fit:
20181006
step = 0.1
min_error:617.7465408998964
min_test_value:4.000000000000003
min_test_value_2:5.9999999999999964

20181007
step = 0.1
min_error:588.9481363632256
min_test_value:3.9000000000000026
min_test_value_2:5.9999999999999964

20181008
step = 0.1
min_error:1495.0487391574018
min_test_value:4.0
min_test_value_2:5.899999999999997

20181009
step = 0.1
min_error:1529.1246208966018
min_test_value:4.0
min_test_value_2:5.899999999999997

20181010
step = 0.1
min_error:1715.047723281613
min_test_value:4.0
min_test_value_2:5.899999999999997

step=0.01
min_error:1549.5206756970797
min_test_value:4.100000000000003
min_test_value_2:6.039999999999978

20181018
step = 0.1
min_error:2701.610113688168
min_test_value:4.900000000000004
min_test_value_2:5.9999999999999964

20181023
min_error:704.6164732327438
min_test_value:3.99871688111845
min_test_value_2:5.499999999999998
central_value = 5.0

20181025
step = 0.1
min_error:525.3516103077461
min_test_value:3.99871688111845
min_test_value_2:5.499999999999995
central_value = 4.0

step = 0.1
min_error:525.3516103077461
min_test_value:3.99871688111845 => 55m
min_test_value_2:5.499999999999998 => 245m
central_value = 5.0
'''


# define distance coordinates,assuming z coodinates 4.05m per level
def distance_match(node_num):
	distance = {
		1: [30.27,56.48,2.025],
		2: [38.72,124.19,2.025],
		3: [62.59,49.56,16.2],
		4: [38.72,124.19,12.15],
		5: [88.08,54.3, 12.15],
		6: [30.27, 79.26, 0],
		7: [38.72, 124.19 ,-2.025],
		8: [38.72, 124.19,16.2],
		9: [65.5, 104.75,2.025],
		10:[69.71, 105.65, 12.15],
		12:[62.59, 49.56, 12.15],
		13:[43.08, 52.39, 16.2],
		14:[458.8,256.21, 14.175],
		15:[113.94, 11.32, 12.15],
		16:[294.48,	0, 14.175],
		18:[247.1,	81.27, 13.16],
		19:[438.58, 283.66, 14.175],
		20:[380.01,	259.85, 14.175],
		21:[380.01, 233.41,	14.175],
		22:[276.47,	207,14.175],
		23:[181.52,	188.79,	0],
		24:[438.58, 283.66,	18.225],
		25:[170.19, 8.31, 13.16],
		26:[302, 118, 14.175],
		27:[351.12,15.8, 14.175],
		28:[351.12,15.8, 22.275]
	}
	return distance.get(node_num,"Invalid node number")

# calculate euclidean distances between two sensors
def square_difference(list_1,list_2):
	return ((float(list_1[0]) - float(list_2[0]))**2 + (float(list_1[1]) - float(list_2[1]))**2 + (float(list_1[2]) - float(list_2[2]))**2)**(1/2.0)

# calculate each device distance
def distance_calc(process_dict):
	trajectory_dict = {}
	for device in process_dict.keys():
		trajectory_dict[device] = []
		keylist = process_dict[device].keys()
		keylist.sort(key=int)
		for key in keylist:
			for node_num in process_dict[device][key].keys():
				trajectory_dict[device].append(node_num)
	distance_dict = {}
	for device in trajectory_dict.keys():
		distance_dict[device] = 0
		node_list = trajectory_dict[device]
		for i in range(0, len(node_list) - 1):
			list_old = distance_match(node_list[i])
			list_new = distance_match(node_list[i + 1])
			distance_dict[device] += square_difference(list_old,list_new)

		distance_dict[device]  = int(distance_dict[device])

	return distance_dict

# generate power law (based on distance) and pdf function plot
def distance_pdf(distance_dict):
	distance_values = distance_dict.values()

	# avoid distance = 0
	distance_values = [distance for distance in distance_values if distance != 0]
	length = len(distance_values)
	
	# count each distance value has how many devices
	distance_calc_hist = {}
	for value in distance_values:
		if value not in distance_calc_hist.keys():
			distance_calc_hist[value] = 1
		else:
			distance_calc_hist[value] += 1
	# calculate pdf function
	for value in distance_calc_hist.keys():
		distance_calc_hist[value] = distance_calc_hist[value] / float(length)

	X_axis = []
	Y_axis = []
	for key,value in distance_calc_hist.items():
		X_axis.append(key)
		Y_axis.append(value)

	X = np.log(np.asarray(X_axis))
	Y = np.log(np.asarray(Y_axis))
	plt.xlabel('log distance')
	plt.ylabel('log P(distance)')
	plt.scatter (X,Y)

	slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X, Y)
	print [slope,intercept,r_value,p_value,std_err]
	plt.plot(X, X*slope + intercept, 'r')
	plt.title('Power Law between #devices and average distance')
	plt.show()

	return distance_calc_hist

# generate rank-freq plot
def distance_rank(distance_values):
	# no overloading in python, so comment out here, distance_dict
	# distance_values = distance_dict.values()
	distance_values.sort(reverse = True)
	rank = np.arange(1,len(distance_values) + 1)
	X = np.log(np.asarray(distance_values))
	Y = np.log(rank)
	plt.scatter(X,Y)
	# split the curve into two lines, test_value is X coordinate of splitting point
	min_error = sys.maxint
	min_test_value = sys.maxint
	min_test_value_2 = sys.maxint
	central_value = 5.0
	for test_value in np.arange(np.min(X),central_value,0.1):
		for test_value_2 in np.arange(central_value,np.max(X),0.1):
			X1 = X[X > test_value_2]
			X2 = X[X > test_value]
			X2 = X2[X2 <= test_value_2]
			X3 = X[X<=test_value]
			Y1 = Y[:len(X1)]
			Y2 = Y[len(X1):len(X1) + len(X2)]
			Y3 = Y[len(X1) + len(X2):]
			# slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X1, Y1)
			# slope_2, intercept_2, r_value_2, p_value_2, std_err_2 = scipy.stats.linregress(X2, Y2)
			# Z1 = np.polyfit(X1,Y1,1,full=True)
			std_err = np.sum((np.polyval(np.polyfit(X1, Y1, 1), X1) - Y1)**2)
			# Z2 = np.polyfit(X2,Y2,1,full=True)
			std_err_2 = np.sum((np.polyval(np.polyfit(X2, Y2, 1), X2) - Y2)**2)
			std_err_3 = np.sum((np.polyval(np.polyfit(X3, Y3, 1), X3) - Y3)**2)
			curr_error = std_err + std_err_2 + std_err_3

			if min_error > curr_error:
				min_error = curr_error
				min_test_value = test_value
				min_test_value_2 = test_value_2
    
	print 'min_error:' + str(min_error)
	print 'min_test_value:' + str(min_test_value)
	print 'min_test_value_2:' + str(min_test_value_2)
	X1 = X[X > min_test_value_2]
	X2 = X[X > min_test_value]
	X2 = X2[X2 <= min_test_value_2]
	X3 = X[X <= min_test_value]
	Y1 = Y[:len(X1)]
	Y2 = Y[len(X1):len(X1) + len(X2)]
	Y3 = Y[len(X1) + len(X2):]
	# print [slope,intercept,r_value,p_value,std_err]
	slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X1, Y1)
	plt.plot(X1, X1*slope + intercept, 'r')
	# print [slope,intercept,r_value,p_value,std_err]
	slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X2, Y2)
	plt.plot(X2, X2*slope + intercept, 'r')
	slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X3, Y3)
	plt.plot(X3, X3*slope + intercept, 'r')

	# slope,intercept = np.polyfit(X1,Y1,1)
	# plt.plot(X1, X1*slope + intercept, 'r')
	# slope,intercept = np.polyfit(X2,Y2,1)
	# plt.plot(X2, X2*slope + intercept, 'r')

	plt.xlabel('log distance')
	plt.ylabel('log rank')
	plt.title('Rank-frequency plot of traveling distance')
	plt.show()
	return distance_values


# combine distance dictionaries in 5 days
def combine_distance_dict(distance_dict,distance_dict_2,distance_dict_3,distance_dict_4,distance_dict_5):
	day_1 = Counter(distance_dict)
	day_2 = Counter(distance_dict_2)
	day_3 = Counter(distance_dict_3)
	day_4 = Counter(distance_dict_4)
	day_5 = Counter(distance_dict_5)

	distance_combined = {}
	distance_combined = day_1 + day_2 + day_3 + day_4 + day_5
	return distance_combined

# get devices that get most nodes
def visit_most_node_device(process_dict):
	# plot trajectory
	trajectory_dict = {}
	count_dict = {}
	for device in process_dict.keys():
		trajectory_dict[device] = []
		count_dict[device] = 0
		node_num_list = []
		keylist = process_dict[device].keys()
		keylist.sort(key=int)
		for key in keylist:
			for node_num in process_dict[device][key].keys():
				trajectory_dict[device].append(node_num)
				if node_num not in node_num_list:
					node_num_list.append(node_num)
					count_dict[device] += 1
	# print count_dict
	popular_device = dict(Counter(count_dict).most_common(24))
	popular_trajectory = {}

	for device in popular_device.keys():
		popular_trajectory[device] = trajectory_dict[device]

	print popular_trajectory.values()

# plot the tendancy of one-way distance
def one_way_distance(trajectory_dict):
	# count tendancy of one_way distance 
	one_way = {}
	# append every distance in this list
	one_way_count = []
	for device in trajectory_dict.keys():
		node_list = trajectory_dict[device]
		if len(node_list) <= 1:
			continue
		for i in range(0,len(node_list) - 1):
			distance = square_difference(distance_match(node_list[i]),distance_match(node_list[i+1]))
			# distance = (distance // 10) * 10
			if distance == 0:
				continue
			one_way_count.append(distance)
			if distance not in one_way.keys():
				one_way[distance] = 1
			else:
				one_way[distance]+=1
	# ignore if distance = 0
	# del one_way[0]

	# X = np.log(np.asarray(one_way.keys()))
	# Y = np.log(np.asarray(one_way.values()))
	# plt.xlabel('log distance')
	# plt.ylabel('log count')
	# plt.scatter (X,Y)

	# slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X, Y)
	# print [slope,intercept,r_value,p_value,std_err]
	# plt.plot(X, X*slope + intercept, 'r')
	# plt.title('Power Law between count and one-way distance')
	# plt.show()
	return one_way,one_way_count

# count node_num within sij in radiation model
def node_in_distance(node_i,node_j,node):
	distance = square_difference(distance_match(node_i),distance_match(node_j))
	# any node that is within this distance
	inside_node = [node_num for node_num in node if square_difference(distance_match(node_i),distance_match(node_num)) <= distance]
	return inside_node









