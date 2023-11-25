from transformar_a_matriu import shortestPath

def genera_csv_out(ordered_ticket_entries, planogram, user):
    rows_to_add=[]
    time=0
    lastCheck = ordered_ticket_entries[0]
    for checkpoint in ordered_ticket_entries[1:]:
        newPath = shortestPath(lastCheck, checkpoint, planogram)
        for step in newPath:
            x,y = step

        
            # first, the time it delays to pick an item
            if(step.picking):
                for i in range(0,user.picking_seconds):
                    # TODO: TAKE INTO ACCOUNT THE THE NUMBER OF TIMES IT HAS BEEN PICKED
                    # TODO: Make sure to check if is picking or not
                    rows_to_add.append([user.customer_id, user.ticket_id, x, y, step.picking, time])
                    time+=1
        
            for i in range(0,user.step_seconds):
                rows_to_add.append([user.customer_id, user.ticket_id, x, y, step.picking, time])
                time+=1
            
            
            


    
    

file_name = "out.csv"
headers = ['customer_id', 'ticket_id','x','y','picking', 'x_y_date_time']
create_csv(file_name, headers)

append_to_csv(file_name, rows_to_add)
