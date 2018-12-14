# BLE_Campus_Mobility_Sensing
Summer 2018 project using Raspeberry Pi 0Ws distributed across campus to determine population mobility patterns by tracking Bluetooth device signatures.

# Visualization
## All of the files are located in data_processing/interference/  
### filter_data: filter  out the static device at each node. usage: python filter_data 2018-08-11
### graph helper: it can help you generate csv for gephi from the raw data after filter data. For detail usage look at the file
### collection_analysis: which is to build 3D model it may be useful for your future work to build 3D model.
### data_recovery/: the data recovery algoritm I buit for some file which may only lose small part of the information. To -achieve this, It will just assume there is no device file
### around that area during the time the node was down
### data_analysis/: which is for collective analysis to do some data visulization you may not need this file in the future

# ML Models
## MLMODEL/ : all of the models are writen by jupyter notebook.
### RNN/: Please look at this directory for ML model
### VAR.ipynb, the based line model
### Preprocessing.ipynb, preprocess the data before feed into the model which basically do the data cleasning
### Population_Prediction_RNN: the RNN model we built, the parameter which should reproduce the best result for now
### Classfication_Abnormal_Detection: Make use of the model built above and detect abnormal situation
### Classfication_Try: try to convert regression problem to classfication problem with only data preprocessing. NO Model
### *: else are helper function wrote before, just copy from root directory to here for convience 
### *.npy: some data which does not need to recalcaulate every time

## -Regression/: Deprecated 

# Network Model Fitting
## The related files are in the folder netModelFitting/, which is fitting radiation / gravity model with actual data.
### individual_trajectory.py: main file, incorporate helper functions from the rest of files, fulfill the following function:
1. Measure tendancy of number of devices with respect to the distance and time duration (helper function: distance_calc.py, time_duration.py)
2. Fit the flow between every pair of nodes with gravity model and radiation model(in individual_trajectory.py,some helper function in pair_degree_count.py)
3. Measure betweenness centrality (helper function in betweenness_centrality.py)
4. Plot popular trajectory without campus background(helper: plot_popular_trajectory.py)
5. Generate static graph in gephi and pygraphviz (gephi_pygraphviz.py, graph_helper.py)
6. Noise removal and preprocessing(noise_removal.py, create_time_series.py, device_list_time_slot.py, device_class.py, pickle_dump_load.py, recover.py)







