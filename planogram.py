from utils import read_csv_file

class Cell:
    def __init__(self, description=None, picking_x=None, picking_y=None):
        self.description = description
        self.picking_x = picking_x
        self.picking_y = picking_y
        


def get_planogram(file_name):
    planogram = {}
    csv_file = read_csv_file(file_name)
    count = 0
    for row in csv_file:
        if(count != 0):
            elements = row[0].split(';')
            picking_x = None if elements[2] == '' else elements[3]
            picking_y = None if elements[4] == '' else elements[4]
            cell = Cell(elements[2], picking_x, picking_y)
            # planogram[elements[0]][elements[1]] = cell
            row = planogram.get(elements[0],{})
            row[elements[1]] = cell

            planogram[elements[0]] = row

        count+=1
    return planogram


get_planogram('./input/planogram_table.csv')
