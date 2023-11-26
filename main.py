from article_picking_time import get_article_picking_time
from user import get_users_without_ticket_entries, populate_users_with_ticket_entries
from planogram import get_planogram
from tickets import get_tickets
from transformar_a_matriu import transformar_a_problema_lineal, obtenir_assignacions_ordenades
from algorisme import minimum_assignment, algorisme_ineficient,tsp

from pprint import pprint


article_picking_time = get_article_picking_time('./input/hackathon_article_picking_time.csv')
planogram = get_planogram('./input/planogram_table.csv')
users = get_users_without_ticket_entries()
users = populate_users_with_ticket_entries(users)   


user = users.get('c26')

tickets = {} 
for i, ticketEntrie in enumerate(user.ticketEntries):
    tickets[i] = ticketEntrie


matriu = transformar_a_problema_lineal(user, planogram) #fix me, no comptat inicial i

pprint(matriu) 


assignacio_optima = algorisme_ineficient(matriu)

pprint(assignacio_optima)


ordered_ticket_entries = obtenir_assignacions_ordenades(assignacio_optima) 


print(ordered_ticket_entries)



genera_csv_out(ordered_ticket_entries, planogram, tickets)
