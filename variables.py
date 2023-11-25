from article_picking_time import get_article_picking_time
from user import get_users_without_ticket_entries, populate_users_with_ticket_entries
from planogram import get_planogram
from tickets import get_tickets



article_picking_time = get_article_picking_time('./input/hackathon_article_picking_time.csv')


planogram = get_planogram('./input/planogram_table.csv')


users = get_users_without_ticket_entries()
users = populate_users_with_ticket_entries(users)
