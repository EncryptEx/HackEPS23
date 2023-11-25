from article_picking_time import get_article_picking_time
from user import get_users_without_ticket_entries, populate_users_with_ticket_entries
from planogram import get_planogram
from tickets import get_tickets
from transformar_a_matriu import transformar_a_problema_lineal, obtenir_assignacions_ordenades
from algorisme import minimum_assignment



article_picking_time = get_article_picking_time('./input/hackathon_article_picking_time.csv')
planogram = get_planogram('./input/planogram_table.csv')
users = get_users_without_ticket_entries()
users = populate_users_with_ticket_entries(users)   


user = users.get('c1')

matriu = transformar_a_problema_lineal(user, planogram) #fix me, no comptat inicial i

assignacio_optima = minimum_assignment(matriu)

ordered_ticket_entries = obtenir_assignacions_ordenades(assignacio_optima) #fix me

genera_csv_out(ordered_ticket_entries, planogram, user)

ç
rows_to_add = []
segon = 0

while():

    
    



file_name = "out.csv"
headers = ['customer_id', 'ticket_id','x','y','picking', 'x_y_date_time']
create_csv(file_name, headers)

append_to_csv(file_name, rows_to_add)