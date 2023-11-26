from transformar_a_matriu import shortestPath
from tickets import TicketEntry, get_tickets
from article_picking_time import get_article_picking_time, search_article_picking_time
from utils import create_csv, append_to_csv
from datetime import datetime
from transformar_a_matriu import get_article_coords
from datetime import datetime, timedelta


def genera_csv_usuari(index_order, tickets, planogram, usuari, product_offsets, filename):
    
    ordered = orderTicketEntries(tickets, index_order)

    rows_to_add = genera_csv_out(ordered, planogram, usuari, product_offsets)
    append_to_csv(filename, rows_to_add)
      
def orderTicketEntries(ticket_entries, order):
        aux = []
        for i in order:
            aux.append(ticket_entries.get(i))
        return aux

def genera_csv_out(ordered_ticket_entries, planogram, user, product_offsets):
    rows_to_add=[]
    time= user.enter_date_time
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    lastCheck = TicketEntry("paso-entrada", 0, None,  None) 
    for checkpoint in ordered_ticket_entries:
       
        newPath = shortestPath(lastCheck,checkpoint, planogram)
        print(newPath)
        for step in newPath:
            x,y = step
        
            for i in range(int(user.step_seconds)):
                rows_to_add.append([user.id, user.ticket_id, x, y, 0, time.strftime("%Y-%m-%d %H:%M:%S")])
                time += timedelta(seconds=1)
        # first, the time it delays to pick an item

        x, y = get_article_coords(planogram, checkpoint.article_id)
        for j in range(len(checkpoint.quantity)):
            for i in range(int(user.picking_offset) + int(product_offset(checkpoint.article_id, j+1, product_offsets))):
                rows_to_add.append([user.id, user.ticket_id, x, y, 1, time.strftime("%Y-%m-%d %H:%M:%S")])
                time += timedelta(seconds=1)
                
    return rows_to_add

def product_offset(product_id, quantity, product_offsets):
    o1,o2,o3,o4,o5 = search_article_picking_time(product_offsets, product_id)
    if(quantity==1):
        return o1
    elif(quantity==2): return o2
    elif(quantity==3): return o3
    elif(quantity==4): return o4
    else: return o5


