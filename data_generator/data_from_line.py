# creates syntetic data into syntetic_data folder
# the data is created by selecting some points around some line determined by the user, wrt some normal distribution

import numpy as np
import csv

# float slope: slope of the line (a of ax+b)
# float constant: constant of the line (b of ax+b)
# float interval_start: start of the interval to start taking samples from (in the x axis)
# float interval_end: end of the interval to stop taking samples from (in the x axis)
# float error_var: the varience of the normal distribution, to be used to get the deviation from the line
# string file_name: name of the csv file for the syntetic data to be saved to
def generate_client_data(slope, constant, num_of_points, interval_start, interval_end, error_var, file_name):
    if interval_end<=interval_start or num_of_points<=0 or error_var<=0:
        raise Exception("There was an invalid input")
    data = []
    interval_len = interval_end - interval_start
    step_size = interval_len / num_of_points
    step = 0
    for i in range(num_of_points):
        step += step_size
        y_val = (slope * step) + constant
        error = np.random.normal(loc=0, scale = error_var)
        data.append([step, y_val+error])
    with open("syntetic_data/"+file_name+".csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(data)
    return 0

# example usage: generate_client_data(2, 5, 10, 0, 10, 1, "client1")
