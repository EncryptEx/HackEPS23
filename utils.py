# File to host functions that are called between different files

import csv
import os

# read a csv file 
def read_csv_file(file_name):
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        return list(reader)
    

def create_csv(file_name, headers):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(headers)

def append_to_csv(file_name, rows):
    with open(file_name, mode='a', newline='') as file:
 
        writer = csv.writer(file, delimiter=';')
        for row in rows:
            writer.writerow(row)


