import pickle
# store process_dict of a day for future use
def pickle_dump(process_dict,input_date):
	# file_name = '/Users/pengchen/CMU-Summer-Project/CMU_Summer_Project_2018/'+ input_date + '-process-dict.obj'
	file_name = '/Users/pengchen/CMU-Summer-Project/CMU_Summer_Project_2018/'+ input_date + '-trajectory-dict.obj_10am_6pm'
	file_process = open(file_name,'w')
	pickle.dump(process_dict,file_process)

# restore process_dict of a day to memory
def pickle_load(input_date):
	file_name = '/Users/pengchen/CMU-Summer-Project/CMU_Summer_Project_2018/'+ input_date + '-process-dict.obj'
	# file_name = '/Users/pengchen/CMU-Summer-Project/CMU_Summer_Project_2018/'+ input_date + '-process-dict_without13.obj'
	# file_name = '/Users/pengchen/CMU-Summer-Project/CMU_Summer_Project_2018/'+ input_date + '-trajectory-dict.obj'
	file_handler = open(file_name, 'r')
	process_dict = pickle.load(file_handler)
	return process_dict

def pickle_load_traj(input_date):
	# file_name = '/Users/pengchen/CMU-Summer-Project/CMU_Summer_Project_2018/'+ input_date + '-trajectory-dict.obj'
	file_name = '/Users/pengchen/CMU-Summer-Project/CMU_Summer_Project_2018/'+ input_date + '-trajectory-dict.obj_10am_6pm'
	file_handler = open(file_name, 'r')
	process_dict = pickle.load(file_handler)
	return process_dict