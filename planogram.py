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

def get_article(palnogram, article_id):
    for x,dict in palnogram.items():
        for y,cell in dict.items():
            if cell.description == article_id:
                return cell


def get_article_coords(palnogram, article_id):
    for x,dict in palnogram.items():
        for y,cell in dict.items():
            if cell.description == article_id:
                return x,y

def get_article_coords_pickup(palnogram, article_id):
    for x,dict in palnogram.items():
        for y,cell in dict.items():
            if cell.description == article_id:
                if article_id == "paso-salida" or article_id == "paso-entrada":
                    return x,y
                return cell.picking_x , cell.picking_y


# get_planogram('./input/planogram_table.csv')
