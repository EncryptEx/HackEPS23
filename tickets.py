from utils import read_csv_file

def get_tickets(file_name):
        customers = {}
        csv_file = read_csv_file(file_name)
        count = 0
        for row in csv_file:
            if(count != 0):
                elements = row[0].split(';')
                customers[elements[1]] = {'timestamp': elements[0], 'article_id': elements[2], 'quantity':elements[3], 'ticket_id':elements[4] }
            count+=1
        return customers