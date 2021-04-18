# NAME: Mia Berthier
# ID: 260913316

import doctest
import datetime
import numpy as np
import matplotlib.pyplot as plt

########## HELPERS #######################################################
letters = "abcdefghijklmnopqrstuvwxyz"

def check_temperature(t):
    """(str) --> list
    A function which takes a temperature in string and returns it's value in celsius
    (from celsius or farenheit) as a list.

    >>> check_temperature("22")
    [22.0]
    >>> check_temperature("100")
    [37.78]
    >>> check_temperature("103.3.")
    [39.61]
    """
    #Create an empty list and an empty string
    temperature = ""
    temp = []

    #For every character in the input string
    for e in t:
        #Change "," to "."
        if e == ",":
            temperature += "."
        #If this character isn't a digit, remove it
        elif e.lower() not in letters and e != " " and e != "°":
            temperature += e

    #Make sure that the last character is a digit
    if not temperature[-1].isdigit():
        temperature = temperature[:-1]

    #If the temperature is superior to 45, we assume it's farenheit
    if float(temperature) > 45:
        #Change the temperature to celsius
        temperature = round((float(temperature) - 32) * 5/9, 2)
    #Add this temperature to the list of temperatures
    temp.append(float(temperature))

    return temp

def check_gender(g):
    """ (str) --> str
    Return F, M or X according to the gender which is inputed (whether this gender
    is in french or english.

    >>> check_gender("Woman")
    'F'
    >>> check_gender("non binaire")
    'X'
    >>> check_gender("garçon")
    'M'
    """
    f = ["woman", "female",  "femme", "fille", "girl", "f", "w"]
    m = ["homme", "male", "man", "boy", "garçon", "m", "h"]
    #Check the first letter (or first two letters) of the input to see which gender
    if g.lower() in f:
            sex_gender = "F"
    elif g.lower() in m:
            sex_gender = "M"
    else:
            sex_gender = "X"

    return sex_gender

def temp_str_list(temps):
    """() --> str
    From either a list of floats or a single float, return a string which separates the
    various temperatures with a semi-colon

    >>> temp_str_list([10.2, 11.3, 22.0])
    '10.2; 11.3; 22.0'
    >>> temp_str_list(0)
    '0'
    >>> temp_str_list([39.2])
    '39.2'
    """
    #If the input is a list
    if type(temps) == list:

        #Check if the length is superior to 1
        if len(temps) > 1:
            list_temperatures = []

            #For every character in the list
            for e in temps:

                #If this character is a list, append the string of the first element
                if type(e) == list:
                    list_temperatures.append(str(e[0]))
                #Otherwise append the string of the character 
                else:
                    list_temperatures.append(str(e))
            #Join all the temperatures in the temporary list with ";" as a separator
            temperatures = "; ".join(list_temperatures)

        #If the length is 1, then temperatures are just the string of the element
        else:
            temperatures = str(temps[0])

    #If the input is not a list, return a string of the input
    else:
        temperatures = str(temps)

    return temperatures

##########################################################################

class Patient:
    """ Represents a patient

    Attributes: num, day_diagnosed, age, sex_gender, postal,
    state, temps, days_symptomatic
    """
    #Creating a patient's attributes
    def __init__(self, n, day_diag, a, sex, post, s, temp, day_sympt):
        #Change the string of the number, day of diagnosis and age into an int
        self.num = int(n)
        self.day_diagnosed = int(day_diag)
        self.age = int(a)

        #From the string indicating the gender return M, F, X
        self.sex_gender = check_gender(sex)

        #Check if the three first elements of the postal code are H followed by a
        #number followed by a letter and return that
        if post[0] == "H" and post[1] in "1234567890" and post[2].lower() in letters:
            self.postal = post[: 3]
        #If the postal code is invalid return 000
        else:
            self.postal = "000"

        #Initiate the state of the patient
        self.state = s
        
        #If the first element of the temperature is a letter, set the temperature as 0
        if temp[0].lower() in letters:
            self.temps = 0.0
        #Otherwise return a list of the temperature in celsius
        else:
            self.temps = check_temperature(temp)

        #Initiate an empty string
        day_symptomatic = ''
        #For every character in the input of days_sympt
        for e in day_sympt:
            #If this character is a digit add it to the string
            if e.isdigit():
                day_symptomatic += e
        #Return this number as a string
        self.days_symptomatic = int(day_symptomatic)

    def __str__(self):
        """
        A function which returns the Patient's attributes in a line
        separated by tabs.
        
        >>> p = Patient('0', '0', '42', 'Woman', 'H3Z2B5', 'I', '102.2', '12')
        >>> p1 = Patient('1', '1', '54', 'F', 'H4X', 'I', '40,0 C', '13')
        >>> str(p)
        '0\\t42\\tF\\tH3Z\\t0\\tI\\t12\\t39.0'
        >>> str(p1)
        '1\\t54\\tF\\tH4X\\t1\\tI\\t13\\t40.0'
        """
        #Put the temperatures in a string of temperatures separated by ";"
        temperatures = temp_str_list(self.temps)

        #Make a list of all the Patient's attributes in string format
        attributes = [str(self.num), str(self.age), self.sex_gender, self.postal,
                      str(self.day_diagnosed), self.state, str(self.days_symptomatic),
                      temperatures]

        #Return the attributes in a single line separated by a tab
        return "\t".join(attributes)

    def update(self, p2):
        """ (Patient) --> None
        A function which updates the patient with the changed values of
        the same patient. If they are different patients, an AssertionError
        is raised.

        >>> p = Patient('0', '0', '42', 'Woman', 'H3Z2B5', 'I', '102.2', '12')
        >>> p1 = Patient('0', '1', '42', 'F', 'H3Z', 'I', '40,0 C', '13')
        >>> p.update(p1)
        >>> str(p)
        '0\\t42\\tF\\tH3Z\\t0\\tI\\t13\\t39.0; 40.0'
        """
        #Check if the number, gender and postal code are the same
        if self.num == p2.num and self.sex_gender == p2.sex_gender and self.postal == p2.postal:
            #Update the patient's days symptomatic, their state and add the temperature
            self.days_symptomatic = p2.days_symptomatic
            self.state = p2.state
            self.temps.append(p2.temps)

        #If this is not the same patient raise an AssertionError
        else:
            print(self, p2)
            raise AssertionError



def stage_four(input_filename, output_filename):
    """ (str, str) --> dict

    >>> p_short = stage_four('stage3_short.tsv', 'stage4_short.tsv')
    >>> len(p_short)
    6
    >>> str(p_short[0])
    '0\\t28\\tM\\tH3C\\t0\\tI\\t7\\t39.0; 40.92; 40.0'
    >>> p = stage_four('stage3.tsv', 'stage4.tsv')
    >>> len(p)
    1826
    >>> str(p[0])
    '0\\t28\\tM\\tH3C\\t0\\tI\\t13\\t39.0; 40.92; 40.0; 41.0; 39.4; 37.0; 39.0; 37.58; 37.2'
    """
    #Open both input_filename and output_filename
    f_read = open(input_filename, 'r', encoding = 'utf-8') 
    f_change = open(output_filename, 'w', encoding = 'utf-8') 

    #Create a list with all the lines of the input file
    all_lines = f_read.readlines()

    #Create a dictionary where we will store all the patients
    patients = {}

    #Iterate through every line
    for line in all_lines:

        #Split the line into the different columns on the line
        columns = line.split("\t")

        #Create a patient
        num = columns[1]
        days_diag = columns[2]
        age = columns[3]
        sex = columns[4]
        post = columns[5]
        state = columns[6]
        temp = columns[7]
        days_symp = columns[8]
        
        line_patient = Patient(num, days_diag, age, sex, post, state, temp, days_symp)

        #If the patient is a new patient add it to the dictionary
        if int(num) not in patients:
            patients[int(num)] = line_patient #The value being the Patient object
        else:
            #Otherwise, update the existing patient with the new record
            patients[int(num)].update(line_patient)

    #Create a list in which you will put the strings of all the patients in the dict
    updated_patients = []
    for k in patients:
        updated_patients.append(str(patients[k]))

    #Write in the output file each element of the list on a new line
    f_change.write("\n".join(updated_patients))
        
    return patients
    
    
def fatality_by_age(dict_patients):
    """ (dict) --> list
    A function which takes a dictionary of patients and creates a plot
    of the probability of death for each age (rounding the ages to the
    nearest multiple of 5).
    
    >>> p = stage_four('stage3.tsv', 'stage4.tsv')
    >>> fatality_by_age(p)
    [1.0, 1.0, 1.0, 1.0, 0.9375, 1.0, 1.0, 1.0, 1.0, 0.9166666666666666, 0.9230769230769231, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    """
    death_by_age = []

    #Create a dict of all the ages and their number of dead
    #And one for the recovered patients
    dead_by_ages = {}
    recovered_by_ages = {}
    for k in dict_patients:
    
        #Round all the patients ages to the nearest 5
        dict_patients[k].age = 5 * round(dict_patients[k].age/5)

        #Initiate the patient if the age has not yet been seen
        if dict_patients[k].age not in dead_by_ages:
            dead_by_ages[dict_patients[k].age] = 0
            recovered_by_ages[dict_patients[k].age] = 0

        #If the patient died or recovered, add one to the specific group
        if dict_patients[k].state == "D":
            dead_by_ages[dict_patients[k].age] += 1
        elif dict_patients[k].state == "R":
            recovered_by_ages[dict_patients[k].age] += 1

    #Create a list of all the ages sorted from youngest to oldest
    x_age = sorted(dead_by_ages)

    #Create a list of all the probability of 
    y_dead = []
    for e in x_age:
        if dead_by_ages[e] != 0:
            probability_fatality = dead_by_ages[e]/(dead_by_ages[e]+recovered_by_ages[e])
        else:
            probability_fatality = 1.0
        y_dead.append(probability_fatality)

    #Create an array for each of these lists
    dead = np.array(y_dead)

    #Let the x-axis be represented by the different ages of the population
    x = np.array(x_age)

    #Plot the line of proportionality of death for every age
    plt.plot(x, dead, '-b')
    plt.ylim((0, 1.2))

    #Name the title, legend and axis of the figure
    plt.title("Probability of death vs age, by Mia Berthier")
    plt.xlabel("Age (to nearest 5)")
    plt.ylabel("Deaths / (Deaths + Recoveries)")

    #Save this figure as a png
    plt.savefig("fatality_by_age.png")

    return y_dead




if __name__ == "__main__":
    doctest.testmod()






    
