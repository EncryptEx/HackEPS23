from utils import read_csv_file

# Timings contains an array of 5 timings
def get_customers_properties(file_name):
    customers = {}
    csv_file = read_csv_file(file_name)
    count = 0
    for row in csv_file:
        if(count != 0):
            elements = row[0].split(';')
            customers[elements[0]] = {'step_seconds': elements[1], 'picking_offset': elements[2]}
        count+=1
    return customers

