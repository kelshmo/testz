module_reading.py
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

import csv # importing CSV module to work with comma separated data.

def enumerate_columns(csv_file_location):
    filename = csv_file_location # reading the file, we can give a path as well.
    with open (filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

    # enumerate()is a pre function and return the index and the value

    for index, column_header in enumerate(header_row):
        print(index, column_header)
enumerate_columns('125.csv')


"""
this function recive a csv file or path as a parameter and
return a list of dictionaries per example, each and single one
unique.

# side note, 
# dialect main pourpose is to remove any lead space while parsing the csv file.

"""
def read_file(csv_file_location):
    csv.register_dialect('readDialect', skipinitialspace=True, strict=True)
    file = csv.DictReader(open(csv_file_location), dialect='readDialect')
    instance_list = []
    for data in file:
        instance_list.append(data) # or path  "path"
    return instance_list
instance_list = read_file('125.csv')
print(instance_list)

"""
This function will <count> how many <Developer_Country> s are

"""
def process_data(instance_list):
    country_list = []
    for instance_data in instance_list:
      country_list.append(instance_data["Developer_Country"])
    country_data = {}
    for country_name in set(country_list):
        country_data[country_name] = country_list.count(country_name)
    return country_data

dictionary = process_data(instance_list)
print(dictionary)

"""

This Fucntion will write a report about our findings
"""
def write_report(dictionary, report_file):
    with open(report_file, "w+") as f:
        for k in sorted(dictionary):
         f.write(str(k)+':'+ str(dictionary[k])+'\n')
        f.close()
write_report(dictionary, "report.txt")