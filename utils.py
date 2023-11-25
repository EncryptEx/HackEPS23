# File to host functions that are called between different files

import csv
import os

# read a csv file 
def read_csv_file(file_name):
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        return list(reader)
    