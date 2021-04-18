# NAME: Mia Berthier
# ID: 260913316

import doctest

########    HELPERS  ######################################

def get_max_from_dict(d):
    """ (dict) --> str
    A function which returns the key which the largest value in
    a dict.

    >>> get_max_from_dict({'a': 20, 'b': 7, 'c': 13, 'd': 22})
    'd'
    >>> get_max_from_dict({'a': 1, 'b': 0, 'c': 0})
    'a'
    """
    #Initiate the maximum value as 0
    max_value = 0
    maximum = 0

    #Iterate through every key in the dict
    for k in d:

        #If the value of the key is larger than the current maximum
        #value, set it as the new maximum value
        if d[k] > max_value:
            max_value = d[k]
            #Let the key be the new maximum
            maximum = k

    return maximum

#########################################################

def which_delimiter(s):
    """(str) --> str
    A function which returns the most commonly used delimiter
    in a single line of string.

    >>> which_delimiter('0 1 2,3')
    ' '
    >>> which_delimiter('0\\t2 3,4,5,6\\t7')
    ','
    """
    #Create an empty dict
    delimiters = {' ': 0, ',': 0, '\t': 0}

    #Iterate through every character in the string,
    for c in s:

        #when there is one of the delimiters (space, comma, tab)
        #add one to the value
        if c in delimiters:
            delimiters[c] += 1


    #Check that not all the values of the dict are equal to 0
    if get_max_from_dict(delimiters) == 0:
        raise AssertionError("There are no commas, tabs or spaces")

    return get_max_from_dict(delimiters)




def stage_one(input_filename, output_filename):
    """(str, str) --> int
    A function which rewrites the input file in an output file with the
    following changes:
        - All text is uppercase
        - The most common delimiter is changed to tab
        - Change all / or . in dates to hyphens

    >>> stage_one('260913316.txt', 'stage1.tsv')
    3000
    >>> stage_one('260913316-short.txt', 'stage1-short.tsv')
    10
    """
    #Open the file called "input_filename" and the file 'output_filename'
    f_read = open(input_filename, 'r', encoding = 'utf-8') #for reading
    f_change = open(output_filename, 'w', encoding = 'utf-8') #for appending

    #Create a list with one string per line
    all_lines = f_read.readlines()

    #Create a counter
    count_lines = 0

    for e in all_lines:            
        #Change all text to be uppercase
        e = e.upper()
        #Change the most common delimiter to tab
        e = e.replace(which_delimiter(e), '\t')
        #Change all / or .  to hyphens
        e = e.replace('/', '-')
        e = e.replace('.', '-')

        #Append this string to the output file
        f_change.write(e)

        #Count one line
        count_lines += 1

    return count_lines


    

def stage_two(input_filename, output_filename):
    """ (str, str) --> int

    >>> stage_two('stage1.tsv', 'stage2.tsv')
    3000
    >>> stage_two('stage1-short.tsv', 'stage2-short.tsv')
    10
    """
    #Open both input_filename and output_filename
    f_read = open(input_filename, 'r', encoding = 'utf-8') 
    f_change = open(output_filename, 'w', encoding = 'utf-8') 

    #Create a list with all the lines of the input file
    all_lines = f_read.readlines()

    count_lines = 0
    
    #Iterate through every line
    for line in all_lines:

        #Split the line into the different columns on the line
        columns = line.split("\t")

        #If the length of there are more than 9 columns
        if len(columns) != 9:

            #Check if the postal code spans two columns
            c = columns[6].lower()
            if c[0] not in 'imdrn':
                #if so, merge the two postal code columns
                columns[5 : 7] = [''.join(columns[5 : 7])]
                    
            if len(columns) != 9:
                #Otherwise merge the two temperature columns
                columns[7 : 9] = [','.join(columns[7 : 9])]

        #Replace the '-' with '.' in the temperatures
        columns[7] = columns[7].replace('-', '.')

        changed_line = "\t".join(columns)
        f_change.write(changed_line)

        count_lines += 1

    return count_lines


if __name__ == "__main__":
    doctest.testmod()
