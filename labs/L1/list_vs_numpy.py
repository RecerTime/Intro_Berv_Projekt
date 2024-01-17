#!/usr/bin/env python3
import time
import numpy as np
from math import sin, pi

print("---------------------------------------------------------")
print("This program compares the execution times of vector computations using lists and NumPy-arrays.")
print("---------------------------------------------------------")
print("Measuring execution time...")

# Vector size
N = int(1e7)

# Python list
startTime_list = time.time()

x_list = list(range(N))
y_list = [sin(2*pi/N*x) for x in x_list]

endTime_list = time.time()

# Numpy array
startTime_arr = time.time()

x_arr = np.arange(0,N)
y_arr = np.sin(2*pi/N*x_arr)

endTime_arr = time.time()

print("Elapsed time with list: {:f} seconds\nElapsed time with NumPy array: {:f} seconds".format(endTime_list-startTime_list,endTime_arr-startTime_arr))
