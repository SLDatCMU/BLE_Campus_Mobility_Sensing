import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import pickle
import datetime
from random import shuffle

## BEGIN CONSTANT AND DATA DEFINITIONS ##

# Data to visualize
test_data = pickle.load(open("2018-10-09-process-dict.obj", "rb"))

# Time and date constants, corresponds to test_data object format
# (time in minutes from 2400 UST)
DATE = datetime.datetime(2018,10,9)
START_TIME = 0
END_TIME = 1440

# Mapping between nodes and GPS approximate location
X_MAX = 500.0
Y_MAX = 300.0
Z_MAX = 20.0
LOCATION_DICTIONARY = {
  1:  np.array([30.27 , 56.48 , 0     ]).reshape((3,1)),
  2:  np.array([38.72 , 124.19, 12.15 ]).reshape((3,1)),
  3:  np.array([62.59 , 49.56 , 16.2  ]).reshape((3,1)),
  4:  np.array([38.72 , 124.19, 12.15 ]).reshape((3,1)),
  5:  np.array([88.08 , 54.3  , 12.15 ]).reshape((3,1)),
  6:  np.array([30.27 , 79.26 , 0     ]).reshape((3,1)),
  7:  np.array([38.72 , 124.19, 0     ]).reshape((3,1)),
  8:  np.array([38.72 , 124.19, 16.2  ]).reshape((3,1)),
  9:  np.array([65.5  , 104.75, 0     ]).reshape((3,1)),
  10: np.array([69.71 , 105.65, 12.15 ]).reshape((3,1)),
  12: np.array([62.59 , 49.56 , 12.15 ]).reshape((3,1)),
  13: np.array([43.08 , 52.39 , 16.2  ]).reshape((3,1)),
  14: np.array([458.8 , 256.21, 14.175]).reshape((3,1)),
  15: np.array([113.94, 11.32 , 12.15 ]).reshape((3,1)),
  16: np.array([294.48, 0     , 14.175]).reshape((3,1)),
  18: np.array([247.1 , 81.27 , 12.15 ]).reshape((3,1)),
  19: np.array([438.58, 283.66, 14.175]).reshape((3,1)),
  20: np.array([380.01, 259.85, 14.175]).reshape((3,1)),
  21: np.array([380.01, 233.41, 14.175]).reshape((3,1)),
  22: np.array([276.47, 207   , 14.175]).reshape((3,1)),
  23: np.array([181.52, 188.79, 0     ]).reshape((3,1)),
  24: np.array([438.58, 283.66, 16.2  ]).reshape((3,1)),
  25: np.array([170.19, 8.31  , 12.15 ]).reshape((3,1)),
  26: np.array([302   , 118   , 14.175]).reshape((3,1)),
  27: np.array([0     , 0     , 0     ]).reshape((3,1)),
  28: np.array([0     , 0     , 0     ]).reshape((3,1)),
}

# Processing constants
GAUSSIAN_SIGMA = 12
SAMPLE_WINDOW_RANGE = 20

# Figure constants
FIGURE_TITLE = 'Human Mobility on CMU Campus [Test Visualization]'
FIGURE_WIDTH = 7
FIGURE_HEIGHT = 5
DATE_FORMAT = '%A, %B %-d, %Y, %-I:%M:%S%p UTC'
NUM_DEVICES = 150

## END CONSTANT AND DATA DEFINITIONS ##


# Generates line data for a specific device
def generate_line(device_data):
  times = sorted(list(device_data.keys()))
  positions = list(map(lambda t: LOCATION_DICTIONARY[list(device_data[t].keys())[0]], times))

  line = np.zeros((3, END_TIME - START_TIME))

  if not len(times) or len(times) != len(positions): return line

  line[:,START_TIME:times[0]] = positions[0];
  for idx in range(len(times)-1):
    line[:,times[idx]:times[idx+1]] = positions[idx]
  line[:,times[-1]:END_TIME] = positions[-1]

  return ndimage.gaussian_filter1d(line, GAUSSIAN_SIGMA, 1)

# Setting up figure and axes
fig = plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
fig.canvas.set_window_title(FIGURE_TITLE)
ax = p3.Axes3D(fig)

# Setting the axes and title properties
ax.set_xlim3d([0.0, X_MAX])
ax.set_xlabel('X')

ax.set_ylim3d([0.0, Y_MAX])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, Z_MAX])
ax.set_zlabel('Z')

title = ax.set_title(FIGURE_TITLE)

# Run this function every frame, updates data and title text
def update_lines(time, line_data, lines):
    for line, data in zip(lines, line_data):
        line.set_data(data[0:2, time-SAMPLE_WINDOW_RANGE:time])
        line.set_3d_properties(data[2, time-SAMPLE_WINDOW_RANGE:time])
    title.set_text(FIGURE_TITLE + '\n' + \
      (DATE + datetime.timedelta(minutes=time)).strftime(DATE_FORMAT))
    return lines

# Generate line data
devices = list(test_data.keys())
shuffle(devices)
line_data = [generate_line(test_data[device]) for device in devices[:NUM_DEVICES]]

# Creating line objects
lines = [ax.plot(line[0, 0:1], line[1, 0:1], line[2, 0:1])[0] for line in line_data]

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, END_TIME - START_TIME,
	                               fargs=(line_data, lines), interval=2, blit=False)

plt.show()