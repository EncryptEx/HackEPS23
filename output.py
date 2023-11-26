from transformar_a_matriu import shortestPath
from tickets import TicketEntry, get_tickets
from article_picking_time import get_article_picking_time, search_article_picking_time
from utils import create_csv, append_to_csv
from datetime import datetime



def orderTicketEntries(ticket_entries: dict, order: list):
    aux = []
    for i in order:
        aux.append(ticket_entries[i])
    return aux




def genera_csv_out(ordered_ticket_entries, planogram, user):
    rows_to_add=[]
    time=0
    lastCheck = TicketEntry("paso-entrada", 0, None,  None) 
    for checkpoint in ordered_ticket_entries:
        newPath = shortestPath(lastCheck, checkpoint, planogram)
        for step in newPath:
            x,y = step

        
            # first, the time it delays to pick an item
            if(step.picking):
                for j in range(0,len(checkpoint.quantity)):
                    for i in range(0,user.picking_seconds+product_offset(j+1)):
                    # TODO: Make sure to check if is picking or not
                        rows_to_add.append([user.customer_id, user.ticket_id, x, y, step.picking, time])
                        time+=1
        
            for i in range(0,user.step_seconds):
                rows_to_add.append([user.customer_id, user.ticket_id, x, y, step.picking, time])
                time+=1
            

def product_offset(product_id, quantity):
    o1,o2,o3,o4,o5 = search_article_picking_time(product_offsets, product_id)
    if(quantity==1):
        return o1
    elif(quantity==2): return o2
    elif(quantity==3): return o3
    elif(quantity==4): return o4
    else: return o5


def genera_csv_usuari(index_order, tickets, planogram, filename, usuari):
    product_offsets = get_article_picking_time("input/hackathon_article_picking_time.csv")
    ordered = orderTicketEntries(tickets, index_order)

    rows_to_add = genera_csv_out(ordered, planogram, usuari)
    append_to_csv(filename, rows_to_add)

    
        

def genera_csv_out(ordered_ticket_entries, planogram, user):
    rows_to_add=[]
    time=0
    lastCheck = TicketEntry("paso-entrada", 0, None,  None) 
    for checkpoint in ordered_ticket_entries:
        newPath = shortestPath(lastCheck, checkpoint, planogram)
        for step in newPath:
            x,y = step

        
            # first, the time it delays to pick an item
            if(step.picking):
                for j in range(0,len(checkpoint.quantity)):
                    for i in range(0,user.picking_seconds+product_offset(j+1)):
                    # TODO: Make sure to check if is picking or not
                        rows_to_add.append([user.customer_id, user.ticket_id, x, y, step.picking, datetime.strftime("%Y-%m-%d"), time])
                        time+=1
        
            for i in range(0,user.step_seconds):
                rows_to_add.append([user.customer_id, user.ticket_id, x, y, step.picking, time])
                time+=1
    return rows_to_add



    
    

# file_name = "out.csv"
# headers = ['customer_id', 'ticket_id','x','y','picking', 'x_y_date_time']
# create_csv(file_name, headers)

# append_to_csv(file_name, rows_to_add)
