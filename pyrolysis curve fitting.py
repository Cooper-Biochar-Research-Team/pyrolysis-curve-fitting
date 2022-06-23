# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 10:33:22 2022

@author: Aviv Kresch, Xiao Lin, Kyle Wong
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
from sklearn.linear_model import LinearRegression

# Load the data from a csv file and import the data into python
# TODO: Utilize the csvreader to load the columns in the csv file automatically without editing initialization
def load_data(data_sets):
    datafile = 'pyrolysis_python_test_data.csv'

    # Set up the csvreader
    with open(datafile, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        fields = next(csvreader)

        # Iterate through the csv file and add the data to data_sets
        for row in csvreader:
            for i in range(len(data_sets)):
                if row[i] != '':
                    row[i] = float(row[i])
                    data_sets[i].append(row[i])
    return fields

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
    # Find the start time of the reaction
    for time_i in range(len(test_sets[test_i])):
        start_time = 0
        # When the temperature difference is higher than 2°C in 1s for the first time,
        # the current time is considered as the start time
        if np.abs(test_sets[test_i][time_i] - test_sets[test_i][time_i + 1]) > 2:
            start_time = time_i
            print(f'\nFor {name}:')
            print(f'The start time is {start_time}s')
            break

    # Find the end time of the reaction
    for time_i in range(100, len(test_sets[test_i])-1):
        end_time = 420
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

'''
# Subtract the empty sets from the data sets (WIP)
# Issue: the start of temp drop of empty set and data set might not be the same  
def subtraction(empty, test):
    subtracted = []
    for subtract_i in range(len(test)):
        if subtract_i < 2:
            for num1, num2 in zip(test[subtract_i], empty[subtract_i]):
                num = num1 - num2
                print(num)
                subtracted[subtract_i].append(num)
        else:
            for num1, num2 in zip(test[subtract_i], empty[subtract_i - 1]):
                num = num1 - num2
                subtracted[subtract_i].append(num)
    print(subtracted)
    return subtracted
'''

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

    # Use linear regression model to obtain the trend-line and R-square value
    lin_reg = LinearRegression()
    # print(test_temp, reaction_time_sets)
    lin_reg.fit(test_temp, reaction_time_sets)
    r2 = np.round(lin_reg.score(test_temp, reaction_time_sets), 4)
    print(f'\nThe R-square value for the Reaction Time vs. Temperature graph is {r2}')
    # print(lin_reg.coef_, lin_reg.intercept_)
    x = np.linspace(350, 850, 1000)
    y_pred = lin_reg.intercept_ + lin_reg.coef_ * x

    # Plot reaction time vs. temperature plot with the trend-line (Figure 4)
    plt.plot(x, y_pred, linestyle='--')
    plt.scatter(test_temp, reaction_time_sets)

    plt.title("Reaction Time vs. Temperature")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Reaction Time (s)")
    plt.show()

    return 0

# Note: Update the initializations when new columns are added in the csv file)=
def main():
    # Initialization
    empty_set_400C = []
    test_1_400C = []
    empty_set_500C = []
    test_1_500C = []
    test_2_500C = []
    test_1_600C = []
    empty_set_600C = []
    empty_set_700C = []
    test_1_700C = []
    empty_set_800C = []
    test_1_800C = []

    # data_sets includes all data entries, empty_sets includes only empty boat tests,
    # and test_sets includes only pyrolysis tests
    data_sets = [empty_set_400C, test_1_400C, empty_set_500C, test_1_500C, test_2_500C, test_1_600C, empty_set_600C,
                 empty_set_700C, test_1_700C, empty_set_800C, test_1_800C]
    empty_sets = [empty_set_400C, empty_set_500C, empty_set_600C, empty_set_700C, empty_set_800C]
    test_sets = [test_1_400C, test_1_500C, test_2_500C, test_1_600C, test_1_700C, test_1_800C]
    # substracted_sets = subtraction(empty_sets, test_sets)
    reaction_time_sets = np.zeros(len(test_sets))
    test_temp = np.zeros(len(test_sets))

    # The pyrolysis temperature for each test set
    test_temp = np.array([400, 500, 500, 600, 700, 800]).reshape((-1, 1))

    # The following labels will be displayed in the graphs (Figure 2-3)
    empty_set_labels = ['400°C', '500°C', '600°C', '700°C', '800°C']
    test_set_labels = ['400°C test 1', '500°C test 1', '500°C test 2', '600°C test 1', '700°C test 1',
                       '800°C test 1']

    fields = load_data(data_sets)
    generate_results(fields, data_sets, empty_sets, test_sets, reaction_time_sets, test_temp, empty_set_labels, test_set_labels)

    return 0

if __name__ == '__main__':  # when this script is run
    main()
