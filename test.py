from article_picking_time import get_article_picking_time
from user import get_users_without_ticket_entries, populate_users_with_ticket_entries
from planogram import get_planogram
from tickets import get_tickets
from transformar_a_matriu import trobarMinims, transformar_a_problema_lineal, obtenir_assignacions_ordenades, optimitzarMatriuCostos, shortestPath, reduirFilesColumnes
from algorisme import minimum_assignment, algorisme_ineficient,tsp

from pprint import pprint
import numpy as np

'''
article_picking_time = get_article_picking_time('./input/hackathon_article_picking_time.csv')
planogram = get_planogram('./input/planogram_table.csv')
users = get_users_without_ticket_entries()
users = populate_users_with_ticket_entries(users)   




user = users['c2']

tickets = {}
for i, ticketEntrie in enumerate(user.ticketEntries):
    tickets[i] = ticketEntrie

#pprint(tickets)


# Define a sample cost matrix and the number of rows to reduce
cost_matrix = np.array([    
    [0,  20,  30, 40, 50, 60, 70],
    [20, 100, 2, 35, 45, 55, 65],
    [30, 25,  0,  30, 40, 50, 12],
    [40, 35,  30, 0,  35, 45, 55],
    [50, 45,  40, 35, 3,  40, 50],
    [60, 3,  50, 45, 40, 0,  45],
    [70, 65,  60, 55, 50, 45, 0]])

'''

'''# Example usage
cost_matrix = np.array([
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
])

reduced_matrix, merged_indices = optimitzarMatriuCostos(cost_matrix, 3)
print("Reduced Matrix:\n", reduced_matrix)
print("Merged Indices:", merged_indices)

'''


cost_matrix = np.array([
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
])

print(trobarMinims(cost_matrix))
print(reduirFilesColumnes(cost_matrix, 1,0))