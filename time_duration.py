import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import sys
# get the dictionary(Time duration as x axis, #devices as y axis)
'''
20181018
time_duration_plot
[-1.53832129010608, 9.924532816835804, -0.9422748532006487, 4.0672275449130213e-271, 0.022977305610576797]
'''
def time_duration_create(process_dict):
	time_duration = {}
	# mini_length = get_mini_length(device_list)
	# for num in range(0,len(device_list)):
	# for time_slot in range(0,len(device_list[num])):
	for device_name in process_dict.keys():
		value = process_dict[device_name].values()
		mins = [sum(dictionary.values()) for dictionary in value]
		total_mins = sum(mins)
		time_duration[device_name] = total_mins
		# for device_name in device_list[num][time_slot].keys():
		# for time_slot in range(0,mini_length):
			# if device_name in process_dict.keys():
			# get a preferred node number
			# if time_slot not in node_time_dict[device_name].keys():
			# 	continue
			# num = node.index(node_time_dict[device_name][time_slot])
			# if device_name not in time_duration.keys():
			# 	time_duration[device_name] = device_list[num][time_slot][device_name].count
			# else:
			# 	time_duration[device_name] += device_list[num][time_slot][device_name].count
	for device_name in time_duration.keys():
		if time_duration[device_name] > 720:
			del time_duration[device_name]
    

    # measure every 10s, so divide 6 to get mins
	# time_duration_values = [value / 6.0 for value in time_duration.values()]
	time_duration_values = time_duration.values()
	time_duration_hist = {}
	for value in time_duration_values:
		if value not in time_duration_hist.keys():
			time_duration_hist[value] = 1
		else:
			time_duration_hist[value] += 1
   
	time_duration_classify = {}
	return time_duration,time_duration_hist,time_duration_classify

def set_time_thresh(time_duration, process_dict, thresh):
	# 148.4 mins: division point for time duration 2018-10-25 
	# time < 148.4 err:444.5230058020586 avg:2.039096356890177
	# 148.4 < time < 720 err: 310.3572194739626 avg:1.5595840174570983
	# 60 < time < 720 err: 343.82687332344324 avg:1.5844556374352223
	# 300 < time < 720 avg:1.5781925004219985
	# 394 < time < 720 best avg:0.8678327015986568

	# thresh = 300
	new_dict = {}
	for device in time_duration:
		if time_duration[device] < thresh and time_duration[device] > 0:
			new_dict[device] = process_dict[device]
	return new_dict


def one_way_time_duration(process_dict):
	one_way = {}
	one_way_count = np.array([])
	for device_name in process_dict.keys():
		value = process_dict[device_name].values()
		for time_slot in value:
			one_way_count = np.append(one_way_count, time_slot.values())
		
	one_way_count = -np.sort(-one_way_count)
	print one_way_count
	# assert isinstance(one_way_count,list)
	return one_way_count

def time_duration_rank(one_way_count):
	'''
	20181017
	min_error:1915.2283621571612
	best_test_value:5.0
	[-0.6899207591423634, 11.447509781014379, -0.9885933946373671, 0.0, 0.00030419011644510386]

	20181018
	min_error:1592.800397090897
	best_test_value:5.0
	[-0.7083965073461778, 11.267123172269732, -0.9888047690162348, 0.0, 0.0003382426183827152]

	min_error:1789.8726871518272
	best_test_value:6.0
	[-0.7217936519712289, 11.275696513947311, -0.9894488353716158, 0.0, 0.00033266970908789074]

	'''
	rank = np.arange(1,one_way_count.size + 1)
	X = np.log(one_way_count)
	Y = np.log(rank)
	plt.scatter(X,Y)
	min_std_err = sys.maxint
	best_test_value = 0.0
	for test_value in np.arange(6.0,7.0,0.01):
		X1 = X[X > test_value]
		Y1 = Y[:len(X1)]
		X2 = X[X <= test_value]
		Y2 = Y[len(X1):]
		std_err = np.sum((np.polyval(np.polyfit(X2, Y2, 1), X2) - Y2)**2)
		if std_err < min_std_err:
			min_std_err = std_err
			best_test_value = test_value
	print 'min_error:' + str(min_std_err)
	print 'best_test_value:' + str(best_test_value)
	X1 = X[X > best_test_value]
	X2 = X[X <= best_test_value]
	Y2 = Y[len(X1):]
	slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X2, Y2)
	print [slope,intercept,r_value,p_value,std_err]
	plt.plot(X2, X2*slope + intercept, 'r')

	plt.xlabel('log one_way_time_duration')
	plt.ylabel('log rank')
	plt.title('Rank-frequency plot of one-way time duration')
	plt.show()
	return one_way_count


# combine two time_duration_hist
def time_duration_hist_combine(time_duration,time_duration_2):
	combined_time_duration = dict(time_duration)
	for key in time_duration_2.keys():
		if key in combined_time_duration.keys():
			combined_time_duration[key] += time_duration_2[key]
		else:
			combined_time_duration[key] = time_duration_2[key]
	return combined_time_duration

# plot the time_duration_hist
def time_duration_plot(time_duration_hist):
	# new_list = sorted(time_duration_hist, key=time_duration_hist.get, reverse=True)[:20]
	# print new_list

	X = np.log(time_duration_hist.keys())
	# x = time_duration_hist.keys()
	# y= time_duration_hist.values()
	Y = np.log(time_duration_hist.values())
	# plt.bar(x,y,align='center') # A bar chart
	plt.xlabel('Log Time duration')
	plt.ylabel('Log Number of devices')
	# for i in range(len(y)):
	#     plt.hlines(y[i],0,x[i]) # Here you are drawing the horizontal lines

	# # Find the slope and intercept of the best fit line
	# slope, intercept = np.polyfit(x, y, 1)

	# # Create a list of values in the best fit line
	# abline_values = [slope * i + intercept for i in x]

	# Plot the best fit line over the actual values
	# plt.plot(x, y, '--')
	# plt.plot(x, abline_values, 'b')

	plt.scatter (X,Y)
	# slope, intercept = np.polyfit(X, Y, 1)
	
	slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X, Y)
	print [slope,intercept,r_value,p_value,std_err]
	plt.plot(X, X*slope + intercept, 'r')
	plt.title('Power Law between #devices and time duration')
	plt.show()

# count the population at all nodes
'''
20181026
{1: 2040, 3: 408, 4: 501, 5: 636, 6: 2076, 7: 2489, 8: 1413, 9: 2858, 10: 5400, 12: 1825, 13: 4454, 14: 2696, 15: 3633, 16: 3031, 18: 2177, \
19: 2398, 20: 3118, 21: 7292, 22: 3897, 23: 3116, 24: 5659, 25: 3494, 26: 3103, 27: 2778, 28: 1536}
'''
def count_population(node, process_dict,thresh):
	node_dict = {}
	for node_num in node:
		pop = count_population_helper(node_num,process_dict,thresh)
		node_dict[node_num] = pop
	return node_dict


# count the population at each node
def count_population_helper(node_num,process_dict,thresh):
	node_count = 0
	# time thresh: 20 mins avg_error:2.178867113608047
	# thresh = 20
	for device in process_dict.keys():
		for value in process_dict[device].values():
			if node_num in value.keys() and value[node_num] > thresh:
				node_count += 1
				break
	return node_count 











