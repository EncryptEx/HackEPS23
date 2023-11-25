
from planogram import 
from utils import read_csv_file

class TicketEntry:
    def __init__(self, article_id, quantity, timestamp,ticket_id):
        self.article_id = article_id
        self.quantity = quantity
        self.timestamp = timestamp
        self.ticket_id = ticket_id

    def getCoords(self, planogram):
        return planogram.get(self.article_id,None)
        


def get_tickets(file_name):
    customers = {}
    csv_file = read_csv_file(file_name)
    count = 0
    for row in csv_file:
        if(count != 0):
            elements = row[0].split(';')
            aux = customers.get(elements[1],[])
            aux.append(TicketEntry(elements[2],elements[3],elements[0], elements[4]))
            customers[elements[1]] = aux
        count+=1
    return customers
