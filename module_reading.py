# module_reading.py
"""
This is a Module wrote in Python3, it will be
helpful to have a first observation of csv files.
please forgive any typo
"""


"""
first function, enumerate_colums()
this code will read a CSV file and
enumetarte the columns in order. In Python first position
is 0
"""

import csv
from sys import *

def enumerate_columns(entity.path):
    filename = entity.path 
    with open (filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

    # enumerate()is a pre function and return the index and the value

    for index, column_header in enumerate(header_row):
        print(index, column_header)


"""
this function recive a csv file or path as a parameter and
return as output a list of dictionaries per example, each and single one
unique.
# side note, 
# dialect main pourpose is to remove any lead space while parsing the csv file.

"""
def read_file(entity.path):
    path_to_grab = entity.path
    csv.register_dialect('readDialect', skipinitialspace=True, strict=True)
    file = csv.DictReader(open(path_to_grab), dialect='readDialect')
    instance_list = []
    for data in file:
        instance_list.append(data) # or path  "path"
    return instance_list
instance_list = read_file('')

"""
This function will count categories from a 
categorical column, the idea will be to chek 
what is categorical and what is numerical
"""
def process_data(instance_list):
    categorical_list = []
    for instance_data in instance_list:
        ## looking for categories, also get just numbers.
        ## I need to loo a bit more closelly to this, to make it more general
        ## if the lenght of the column is less than the column, there is categories?
        ## maybe to strict, perhaps 75% of the lenght
            categorical_list.append(instance_data["i"]) ## so we can pass any colum name
            categorical_data = {}
    for categorical_name in set(categorical_list):
        categorical_data[categorical_name] = categorical_list.count(categorical_name)
    return categorical_data

dictionary = process_data(instance_list)

"""
This Fucntion will write a report about our findings
"""
def write_report(dictionary, report_file):
    with open(report_file, "w+") as f:
        for k in sorted(dictionary):
         f.write(str(k)+':'+ str(dictionary[k])+'\n')
        f.close()
write_report(dictionary, "file.extention")
