# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 10:33:22 2022

@author: Aviv Kresch, Xiao Lin, Kyle Wong
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import r2_score

# Load the data from a csv file and import the data into python
# TODO: Utilize the csvreader to load the columns in the csv file automatically without editing initialization

def load_data():
    datafile = 'small_boat_pyrolysis_python_test_data.csv'

    # Set up the csvreader
    with open(datafile, 'r', encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        fields = next(csvreader)
        data_sets = []
        for i in range(len(fields)):
            data_sets.append([])
        # Iterate through the csv file and add the data to data_sets
        for row in csvreader:
            for i in range(len(row)):
                if row[i] != '':
                    row[i] = float(row[i])
                    data_sets[i].append(row[i])
        data_w_labels = []
        for i in range(len(fields)):
            data_w_labels.append(fields[i])
            data_w_labels.append(data_sets[i])
    return data_w_labels

# Calculate the integral (area under the curve) using the trapezoidal rule
def integrate_trapezoidal(h, array, name):
    integral = 0.0
    for i in range(1, len(array)):
        y_a = array[i - 1]
        y_b = array[i]
        y = (y_a + y_b) / 2
        integral += y * h
    print(f'The integral of {name} is {integral: .4}')

# Calculate the reaction time of each test sets
def reaction_time(test_i, test_sets, name):
    # Initialization
    start_time = 0
    end_time = 420

    # Find the start time of the reaction
    for time_i in range(len(test_sets[test_i])):
        # When the temperature difference is higher than 2°C in 1s for the first time,
        # the current time is considered as the start time
        if np.abs(test_sets[test_i][time_i] - test_sets[test_i][time_i + 1]) > 2:
            start_time = time_i
            print(f'\nFor {name}:')
            print(f'The start time is {start_time}s')
            break

    # Find the end time of the reaction
    for time_i in range(100, len(test_sets[test_i])-1):
        # When the temperature difference is lower than 0.15°C in 5s after the major temperature change,
        # the current time is considered as the end time
        if np.abs(test_sets[test_i][time_i] - test_sets[test_i][time_i-5]) <= 0.15:
            end_time = time_i
            print(f'The end time is {end_time}s')
            break

    # Calculate the reaction time from the start time and end time
    reaction_time = end_time - start_time
    print(f'The reaction time is {reaction_time}s')
    return reaction_time

# Generate the text results and plot the graphs
def generate_results(fields, data_sets, empty_sets, test_sets, reaction_time_sets, test_temp, empty_set_labels, test_set_labels):
    print('Integration results:')
    # For each column in the csv file, plot the time-temperature curves (Figure 1) and calculate enthalpy
    for i in range(len(data_sets)):
        plt.plot(data_sets[i], label=fields[i])
        integrate_trapezoidal(1, data_sets[i], fields[i])

    plt.title("Temperature vs. Time (All data)")
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.show()

    # For each empty set, plot the time-temperature curves (Figure 2)
    for i in range(len(empty_sets)):
        plt.plot(empty_sets[i], label=empty_set_labels[i])

    plt.title("Temperature vs. Time (Empty Sets Only)")
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.show()

    # For each data set, plot the time-temperature curves (Figure 3) and calculate the reaction time
    for i in range(len(test_sets)):
        plt.plot(test_sets[i], label=test_set_labels[i])
        reaction_time_sets[i] = reaction_time(i, test_sets, test_set_labels[i])
    plt.title("Temperature vs. Time (Data Sets Only)")
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.show()

    # Plot reaction time vs. temperature plot (Figure 4)
    # lin_reg = LinearRegression()
    # lin_reg.fit([temp], reaction_time_sets)
    plt.scatter(test_temp, reaction_time_sets)

    plt.title("Reaction Time vs. Temperature")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Reaction Time (s)")
    plt.show()

    return 0

# Note: Update the initializations when new columns are added in the csv file)=
def main():
    # Initialization
    data_w_labels = load_data()
    data_sets = []
    fields = []

    for i in range(len(data_w_labels)):
        if i%2==1:
            data_sets.append(data_w_labels[i])
        else:
            fields.append(data_w_labels[i])

    #TODO: separate and match temperature data
    # data_sets includes all data entries, empty_sets includes only empty boat tests,
    # and test_sets includes only pyrolysis tests
    empty_sets = []
    test_sets = []
    empty_set_labels = []
    test_set_labels = []
    for i in range(len(data_w_labels)):
        if "empty" in data_w_labels[i]:    #find a way to get rid of the "empty" in each legend entry
            empty_set_labels.append(data_w_labels[i])
            empty_sets.append(data_w_labels[i+1])
        if "test" in data_w_labels[i]:
            test_set_labels.append(data_w_labels[i])
            test_sets.append(data_w_labels[i+1])


    reaction_time_sets = np.zeros(len(test_sets))

    # The pyrolysis temperature for each test set
    test_temp = []
    for j in test_set_labels:
        for i in range(400,801):
            if str(i) in j:
                test_temp.append(i)

    # The following labels will be displayed in the graphs (Figure 2-3)

    generate_results(fields, data_sets, empty_sets, test_sets, reaction_time_sets, test_temp, empty_set_labels, test_set_labels)

    return 0

if __name__ == '__main__':  # when this script is run
    main()
