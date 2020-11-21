"""
Load data from the dicts and then perform bmi checking for each entry.
Runs the functions using native and numpy methods
"""
import sys
import time
import matplotlib.pyplot as plt
import numpy

from utils import bmi_classify, load_data, parse_bmi_matrix, parse_bmi_native

times = {}

# loading each data
data = load_data(length=int(sys.argv[1]))
data_np = load_data(format="np", length=int(sys.argv[1]))

times["native"] = time.time()
bmis = parse_bmi_native(data)
times["native"] = time.time() - times["native"]

times["matrix"] = time.time()
bmis = parse_bmi_matrix(data_np)
times["matrix"] = time.time() - times["matrix"]

print("Time taken by native python loop: ", times["native"])
print("Time taken by numpy matrix: ", times["matrix"])
print("Numpy is faster than native loops by: ",
      times["native"]/times["matrix"])
