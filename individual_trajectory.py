import sys
from device_list_time_slot import get_device_list,get_device_single_node
from sets import Set
from networkx.drawing.nx_agraph import write_dot
import pylab as pb
# import plotly.plotly as py
import matplotlib.pyplot as plt
from collections import Counter
from math import log
import numpy as np
import scipy.stats
from collections import OrderedDict
from operator import itemgetter
import numpy.polynomial.polynomial as poly
import pickle
import copy
from create_time_series import get_mini_length, get_connection, combine_connection, remove_single_device
from pickle_dump_load import pickle_dump, pickle_load, pickle_load_traj
from distance_calc import distance_match, square_difference, distance_calc, distance_pdf, distance_rank,one_way_distance, node_in_distance
from plot_popular_trajectory import print_popular_individual
from time_duration import time_duration_create, time_duration_plot,one_way_time_duration,time_duration_rank,count_population,count_population_helper,set_time_thresh
from pair_degree_count import plot_popular_pair, count_degree,set_threshold, count_flow, count_flow_helper, count_outflow, count_outflow_helper
from gephi_pygraphviz import dict_to_graph_networkx
from betweenness_centrality import betweenness_centrality
import networkx as nx
from scipy.optimize import curve_fit
import copy
# theory - https://eleanormaclure.files.wordpress.com/2011/03/colour-coding.pdf (page 5)
# kelly's colors - https://i.kinja-img.com/gawker-media/image/upload/1015680494325093012.JPG
# hex values - http://hackerspace.kinja.com/iscc-nbs-number-hex-r-g-b-263-f2f3f4-242-243-244-267-22-1665795040


# node = [3, 12]
# week from 20180803 to 20180805(week 0)
# node = [i for i in range(1,27) if i not in [11,17]]

# week from 20180806 to 20180812(week 1)
# node = [i for i in range(1,27) if i not in [1,2,4,8,9,10,11,15,17,21,23,25]]

# week from 20180813 to 20180816(week 2)
# node = [i for i in range(1,27) if i not in [9,11,17,21,23]]

node = [i for i in range(1,29) if i not in [2, 11, 17]]
# node = [i for i in range(1,29) if i not in [1,10,19,22,24,27,11,17]]

def func(X,a,r,b,k):
	p_i, p_j, dij = X
	return a * p_i + r * p_j - b * dij + k

def fit_gravity(node, node_count, flow, func):
	p_i = []
	p_j = []
	dij = []
	y = []
	for node_i in node:
		for node_j in [node_num for node_num in node if node_num != node_i]:
			if flow[(node_i,node_j)] == 0:
				continue
			p_i.append(node_count[node_i])
			p_j.append(node_count[node_j])
			dij.append(square_difference(distance_match(node_i),distance_match(node_j)))
			y.append(flow[(node_i,node_j)])
	p_i = np.array(np.log(p_i))
	p_j = np.array(np.log(p_j))
	dij = np.array(np.log(dij))
	ydata = np.array(np.log(y))
	# a, r, b, k = 1
	p0 = 1.,1.,1.,1.
	xdata = (p_i,p_j,dij)
	popt, pcov = curve_fit(func, xdata, ydata, p0)
	perr = np.sqrt(np.diag(pcov))
	print perr
	# perr: 20181026 [0.07042082 0.07042082 0.07075266]
	print dij.shape
	print ydata.shape
	plt.scatter(dij, ydata,color = 'r',label = 'actual_flow')
	plt.scatter(dij, func(xdata, *popt), color='g',label = 'gravity_flow')
	plt.xlabel('distance(r)')
	plt.ylabel('flow')
	plt.title("Fitting gravity model in log traveling distance from 10am to 6pm after adding constant")
	plt.legend()
	plt.show()

def func2():
	pass

# keep major time in process_dict
# MIN_VALUE = 14 * 60 = 840
# MAX_VALUE = 22 * 60 = 1320
def keep_regular(process_dict,in_hour,out_hour):
	TIME_FACTOR = 60
	MIN_VALUE = in_hour * TIME_FACTOR
	MAX_VALUE = out_hour * TIME_FACTOR
	for device in process_dict:
		for start_time in process_dict[device].keys():
			if start_time < MIN_VALUE or start_time > MAX_VALUE:
				del process_dict[device][start_time]
	# delete empty device
	new_process_dict = {}
	for device in process_dict:
		if process_dict[device]:
			new_process_dict[device] = process_dict[device]
	return new_process_dict

def fit_radiation(node, node_count, outflow, pair_count):
	actual_flow = []
	radiation_flow = []
	distance_list = []
	# set distance threshold, three segments: 50m and 400m
	DISTANCE_THRESHOLD = 55
	DISTANCE_THRESHOLD_2 = 245
	for node_i in node:
		for node_j in [node_num for node_num in node if node_num != node_i]:
			Ti = outflow[node_i]
			mi = node_count[node_i]
			nj = node_count[node_j]
			inside_node = node_in_distance(node_i,node_j,node)
			sij = 0
			for node_num in inside_node:
				sij += node_count[node_num]
			# exclude population of i and j
			sij = sij - node_count[node_i] - node_count[node_j]
			if ((mi + sij) * (mi + nj + sij)) == 0:
				continue
			# tuple_e = (Ti,mi,nj,sij)
			# print tuple_e
			zij = (Ti * mi * nj) / ((mi + sij) * (mi + nj + sij))
			actual_flow_ij = count_flow_helper(node_i,node_j,pair_count)
			distance_list_ij = square_difference(distance_match(node_i),distance_match(node_j))
			# print zij
			# if zij != 0 and actual_flow_ij != 0 and distance_list_ij > DISTANCE_THRESHOLD and distance_list_ij < DISTANCE_THRESHOLD_2:
			if zij != 0 and actual_flow_ij != 0:
				radiation_flow.append(zij)
				actual_flow.append(actual_flow_ij)
				distance_list.append(distance_list_ij)

	# print actual_flow
	# print radiation_flow

	if len(actual_flow) == 0 or len(radiation_flow) == 0:
		average_err = "no"
		return average_err, 0
	actual_flow = np.array(np.log(actual_flow))
	radiation_flow = np.array(np.log(radiation_flow))
	distance_list = np.array(np.log(distance_list))

	

	# if radiation flow contains all zero, there will be "not converge" error
	if np.count_nonzero(radiation_flow) == 0:
		radiation_flow = radiation_flow + 1
		actual_flow = actual_flow + 1

	



	# make scatter plots for actual_flow and radiation_flow
	# plt.scatter(distance_list, actual_flow, color = 'r',label = "actual_flow")
	# plt.scatter(distance_list, radiation_flow, color = 'g',label = "radiation_flow")

	# actual_err = np.sum((np.polyval(np.polyfit(distance_list, actual_flow, 1), distance_list) - actual_flow)**2)
	# radiation_err = np.sum((np.polyval(np.polyfit(distance_list, radiation_flow, 1), distance_list) - radiation_flow)**2)

	# use predicted radiation flow to fit actual flow
	fit_err = np.sum((np.polyval(np.polyfit(radiation_flow, actual_flow, 1), radiation_flow) - actual_flow)**2)
	average_err = fit_err / float(len(actual_flow))
	# plt.xlabel('distance(r)')
	# plt.ylabel('flow')
	# plt.title("Fitting radiation model in log traveling distance from 10am to 6pm if distance > 55m and < 245m")
	# plt.legend()
	# plt.show()
	fitted_radiation = np.polyval(np.polyfit(radiation_flow, actual_flow, 1), radiation_flow)
	r_value = rsquared(fitted_radiation,actual_flow)

	return average_err, r_value

def rsquared(x, y):
    """ Return R^2 where x and y are array-like."""

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value**2




	

# get process_dict
def process(node, input_date, time_slot):
	device_list = get_device_list(node, input_date, time_slot)
	node_time_dict = get_connection(device_list)
	stop_time_dict = combine_connection(node_time_dict)
	process_dict = remove_single_device(stop_time_dict)
	return process_dict

# get betweeness centrality of different nodes
def between_centrality(process_dict):
	G,node_dict,count = dict_to_graph_networkx(process_dict)
	b = nx.betweenness_centrality(G) 
	plt.bar(b.keys(), b.values(), color='g')
	plt.xlabel('node number')
	plt.ylabel('betweenness_centrality')
	plt.title('Betweenness centrality of nodes')
	plt.show()

# rank-freq plot of time duration
def rank_freq_time(process_dict):
	time_duration,time_duration_hist,time_duration_classify = time_duration_create(process_dict)
	time_duration_plot(time_duration_hist)
	one_way_count = one_way_time_duration(process_dict)
	time_duration_rank(one_way_count)
	# plot_popular_individual(time_duration,process_dict)
	# plot_popular_individual_graphviz(time_duration,process_dict)

# rank-freq plot of distance
def rank_freq_distance(trajectory_dict):
	one_way,one_way_count = one_way_distance(trajectory_dict)
	distance_rank(one_way_count)

def distance_gen(process_dict):
	distance_dict = distance_calc(process_dict)
	distance_bin = distance_hist_plot(distance_dict)


def popular_pair(trajectory_dict):
	pair_count = plot_popular_pair(trajectory_dict)
	thresh = 200
	pair_count = set_threshold(pair_count,thresh)
	popular_pair = dict(Counter(pair_count).most_common(10))
	# plt.bar(popular_pair.keys(), popular_pair.values(), color='g')
	# plt.show()
	return pair_count

# filter out devices by accumulated time duration
def fit_time_thresh(process_dict):
	time_duration,time_duration_hist,time_duration_classify = time_duration_create(process_dict)
	min_error = sys.maxint
	min_thresh = 0
	average_thresh = {}            
	for thresh in range(20,400):
		process_dict = set_time_thresh(time_duration,process_dict,thresh)
		trajectory_dict = print_popular_individual(process_dict)
		pair_count = plot_popular_pair(trajectory_dict)
		node_count = count_population(node, process_dict)
		# fit radiation model
		outflow = count_outflow(node,pair_count)
		average_err = fit_radiation(node, node_count, outflow,pair_count)
		average_thresh[thresh] = average_err
		if average_err < min_error:
			min_thresh = thresh
			min_error = average_err
	print sorted(average_thresh.items(), key=lambda x: x[1])
	return min_thresh, min_error

# fitting time threshold to find the part of actual data that fits radiation model best
def find_best_time_thresh(process_dict):
	thresh_dict = {}
	# min_error = sys.maxint
	# min_thresh = 0
	max_r = 0
	max_thresh = 0

	# begin fitting time threshold to find the part of actual data that fits radiation model best
	for thresh in range(1,400):
		# from 10am to 6pm normal distance
		# best in range(1,100) => error = 0.33820416153318733, thresh = 94

		# 24 hours normal distance
		# best in range(1,100) => error = 0.4577068155506173 thresh = 94
		# best in range(100,200) => error = 0.06536633410077336 thresh=197

		# 24 hours all distance
		# best in range(1,300) => error = 0.08760727448550071 thresh = 231
		# bug in (332,400) => radiation flow either all zeros or empty
		# in (309,332) => actual flow all zeros, make no sense

		# after not setting thresh to print_popular_individual, 24 hours all distance
		# best in range(1,300) => error = 2.0362850623112907 thresh = 171
		# best in range(300,400) => error = 2.252462252776519 thresh = 316

		# r_value
		# best in range(1,400) => r_value = 0.5663226230431848 thresh = 179

		print thresh
		trajectory_dict = print_popular_individual(process_dict)
		pair_count = plot_popular_pair(trajectory_dict)
		node_count = count_population(node, process_dict,thresh)

		# rank_freq_distance(trajectory_dict)
		
	    # fit gravity model
		# flow = count_flow(node, pair_count)
		# fit_gravity(node, node_count, flow, func)

	    # fit radiation model
		outflow = count_outflow(node, pair_count)
		average_err,r_value = fit_radiation(node, node_count, outflow, pair_count)
		# cannot give out error,due to no data in radiation flow
		# if average_err == "no":
		# 	continue

		# thresh_dict[thresh] = average_err
		# if average_err < min_error:
		# 	min_thresh = thresh
		# 	min_error = average_err

		thresh_dict[thresh] = r_value
		if r_value > max_r:
			max_thresh = thresh
			max_r = r_value


	# thresh_file = '/Users/pengchen/CMU-Summer-Project/CMU_Summer_Project_2018/'+ input_date + 'time_thresh.obj'
	# thresh_process = open(thresh_file,'w')
	# pickle.dump(thresh_dict,thresh_process)
	plt.bar(thresh_dict.keys(),thresh_dict.values(),color='g')
	plt.xlabel('time threshold(min)')
	plt.ylabel('r_value')
	plt.title("Time threshold fitting with r_value")
	plt.legend()
	plt.show()

	# print min_error,min_thresh
	print max_r,max_thresh

# One_hour time slot radiation model fitting
def plot_hist_time_slots(process_dict):
	hour_dict = {}
	for in_hour in range(0,22):
		# initialize
		hour_dict[in_hour] = 0
		out_hour = in_hour + 1
		# keep_regular will del record, make a deep copy of process_dict here
		copy_dict = copy.deepcopy(process_dict)
		process_dict_2 = keep_regular(copy_dict, in_hour,out_hour)
		# do not filter out any data here
		# thresh = 0
		# test time threhold that has lowest MSE error, get from find_best_time_thresh
		thresh = 179
		trajectory_dict = print_popular_individual(process_dict_2)
		# print trajectory_dict
		pair_count = plot_popular_pair(trajectory_dict)
		# print pair_count
		node_count = count_population(node, process_dict_2,thresh)
		# print node_count
		outflow = count_outflow(node, pair_count)
		# print outflow
		average_err, r_value = fit_radiation(node, node_count, outflow, pair_count)
		print r_value
		if average_err == "no":
			continue
		hour_dict[in_hour] = r_value
	print hour_dict
	plt.bar(hour_dict.keys(),hour_dict.values(), color='g')
	plt.xlabel('input_hour')
	plt.ylabel('r_value')
	plt.title("one-hour time slot radiation model fitting")
	plt.legend()
	plt.show()




	



def main(node, input_date, time_slot):
	# process_dict = process(node, input_date, time_slot)
	# pickle_dump(process_dict,input_date)
	process_dict = pickle_load(input_date)
	# print len(process_dict.keys())

	# keep major time in process_dict
	# process_dict = keep_regular(process_dict)
	# print len(process_dict.keys())

	find_best_time_thresh(process_dict)
	# plot_hist_time_slots(process_dict)
    
	# fit_time_thresh(process_dict)

	# set staying time threshold to define population
	# time_duration,time_duration_hist,time_duration_classify = time_duration_create(process_dict)
	# thresh = 400
	# process_dict = set_time_thresh(time_duration,process_dict,thresh)
	# trajectory_dict = print_popular_individual(process_dict,thresh)
	# pickle_dump(trajectory_dict,input_date)
	# trajectory_dict = pickle_load_traj(input_date)
	# distance_gen(process_dict)
	# between_centrality(process_dict)
	# rank_freq_time(process_dict)

	# pair_count = plot_popular_pair(trajectory_dict)

	# below is the pair after setting threshold
	# pair_count = popular_pair(trajectory_dict)
	
	# in_connect, out_connect = count_degree(pair_count)
	# # sort pair_count by value
	# popular_pair = dict(Counter(out_connect).most_common())

	# # for key, value in sorted(pair_count.iteritems(), key=lambda (k,v): (v,k)):
	# #     print "%s: %s" % (key, value)
	# plt.bar(popular_pair.keys(), popular_pair.values(), color='g')
	# plt.show()

if __name__ == '__main__':
	input_date = sys.argv[1]	
	time_slot = int(str(sys.argv[2]))
	main(node, input_date, time_slot)
   

