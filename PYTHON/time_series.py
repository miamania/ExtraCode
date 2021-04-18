# NAME: Mia Berthier
# ID: 260913316

import doctest
import datetime
import numpy as np
import matplotlib.pyplot as plt

def date_diff(d1, d2):
    """ (str, str) --> int
    A function which takes two dates and returns how many
    days apart the two dates are, as an integrer

    >>> date_diff('2019-10-31', '2019-11-2')
    2
    >>> date_diff('2019-06-24', '2019-06-20')
    -4
    """
    #Put the date into a list of data: ['year', 'month', 'day']
    d1_data = d1.split('-')
    d2_data = d2.split('-')

    #Create dates with the correct data
    date1 = datetime.date(int(d1_data[0]), int(d1_data[1]), int(d1_data[2]))
    date2 = datetime.date(int(d2_data[0]), int(d2_data[1]), int(d2_data[2]))

    #Find the difference between the two dates
    diff = date1 - date2

    #Return the days between the two dates
    return 0 - diff.days


def get_age(d1, d2):
    """ (str, str) --> int
    A function which takes two dates and returns how many full
    years apart the two dates are.

    >>> get_age('2018-10-31', '2019-11-2')
    1
    >>> get_age('2018-10-31', '2000-11-2')
    -17
    """
    #Check how many days apart the two dates are
    days_apart = date_diff(d1,d2)

    #Divide this number by the number of days in a year and round
    #down to get the number of complete years
    return int(days_apart/365.2425)



def stage_three(input_filename, output_filename):
    """ (str, str) --> dict

    >>> stage_three('stage2-short.tsv', 'stage3_short.tsv')
    {'0': {'I': 1, 'D': 0, 'R': 0}, '1': {'I': 3, 'D': 0, 'R': 0}, '2': {'I': 4, 'D': 2, 'R': 0}}
    >>> stage_three('stage2.tsv', 'stage3.tsv')
    {'0': {'I': 1, 'D': 0, 'R': 0}, '1': {'I': 3, 'D': 0, 'R': 0}, '2': {'I': 6, 'D': 2, 'R': 0}, '3': {'I': 17, 'D': 1, 'R': 0}, '4': {'I': 42, 'D': 3, 'R': 0}, '5': {'I': 101, 'D': 9, 'R': 0}, '6': {'I': 247, 'D': 16, 'R': 0}, '7': {'I': 596, 'D': 40, 'R': 0}, '8': {'I': 1424, 'D': 101, 'R': 3}, '9': {'I': 365, 'D': 23, 'R': 0}}
    """
    #Open the file called "input_filename" and the file 'output_filename'
    f_read = open(input_filename, 'r', encoding = 'utf-8') #for reading
    f_change = open(output_filename, 'w', encoding = 'utf-8') #for appending

    #Create a list with one string per line
    all_lines = f_read.readlines()

    #Determine the index date
    first_line = all_lines[0].split("\t")
    index_date = first_line[2]

    #Initiate the dict which we will return
    final_dict = {}

    #Iterate through every line in the file
    for line in all_lines:
        #Split the line into the different columns on the line
        columns = line.split("\t")

        #Replace the date of each record with the date_diff of that and the
        #index date
        columns[2] = str(date_diff(index_date, columns[2]))

        #Replace the date of birth with the age at the time of index_date
        columns[3] = str(get_age(columns[3], index_date))

        #Add the date of this line to the final dict
        if columns[2] not in final_dict:
            final_dict[columns[2]] = {'I': 0, 'D': 0, 'R': 0}

        #Replace the status with I, R or D
        if columns[6] != "I" and columns[6] != "R" and columns[6] != "D":
            state = columns[6].lower()

            if state[0] == "i": 
                columns[6] = "I"
                
            elif state[0] == "m" or state[0] == "d":
                columns[6] =  "D"

                
            elif state[0] == "r":
                columns[6] = "R"

        #Add one to the corresponding state in the dictionary
        final_dict[columns[2]][columns[6]] += 1

        #Write this new line in the output file
        changed_line = "\t".join(columns)
        f_change.write(changed_line)


    return final_dict



def plot_time_series(stage3):
    """(dict) --> list
    A function which inputs a dict like the return value of stage 3
    and returns a list of lists where each sublist represents a day
    of the pandemic.
    Also creates a png of the evolution of the three stages of the
    sickness over the days of the pandemic and saves it.

    >>> d = stage_three('stage2.tsv', 'stage3.tsv')
    >>> plot_time_series(d)
    [[1, 0, 0], [3, 0, 0], [6, 2, 0], [17, 1, 0], [42, 3, 0], [101, 9, 0], [247, 16, 0], [596, 40, 0], [1424, 101, 3], [365, 23, 0]]
    """
    #Create the list to which we will add all values
    final_list = []

    #Iterate through every key in the dict
    for k in stage3:
        intermediate_list = []

        #Add the values of each key in this list to an intermediate list
        for key in stage3[k]:
            intermediate_list.append(stage3[k][key])

        #Append this list to the final list and start over
        final_list.append(intermediate_list)

    #Create lists of all the values of a certain stage of the pandemic
    inf_values = []
    dead_values = []
    rec_values = []
    for e in final_list:
        inf_values.append(e[0])
        dead_values.append(e[1])
        rec_values.append(e[2])

    #Create arrays for each of these lists
    inf = np.array(inf_values)
    dead = np.array(dead_values)
    recovered = np.array(rec_values)

    #Let the x-axis be as long as the number of lists we have
    x = np.arange(len(final_list))

    #Plot the three lines for the different stages of the sickness
    plt.plot(x, inf, '-b')
    plt.plot(x, dead, '-g')
    plt.plot(x, recovered, '-y')

    #Name the title, legend and axis of the figure
    plt.title("Time seried of early pandemic, by Mia Berthier")
    plt.legend(['Infected', 'Dead', 'Recovered'])
    plt.xlabel("Days into Pandemic")
    plt.ylabel("Number of People")

    #Save this figure as a png
    plt.savefig("time_series.png")

    #Return the list of lists 
    return final_list
        

if __name__ == "__main__":
    doctest.testmod()
    
