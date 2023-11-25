from utils import read_csv_file
from customers_properties import get_customers_properties
from tickets import get_tickets, TicketEntry

class User:
    def __init__(self, id, step_seconds, picking_offset, ticket_id, enter_date_time, ticketEntries):
        self.id = id
        self.step_seconds = step_seconds
        self.picking_offset = picking_offset
        self.ticket_id = ticket_id
        self.enter_date_time = enter_date_time
        self.ticketEntries = ticketEntries    


def get_users_without_ticket_entries():
    customers_properties = get_customers_properties('./input/hackathon_customers_properties.csv')
    users = {}
    for i,v in customers_properties.items():
        users[i] = User(i, v['step_seconds'], v['picking_offset'], None, None, [])
    return users


def populate_users_with_ticket_entries(users):
    ticketEntries = get_tickets('./input/hackathon_tickets.csv')
    
    for userId,ticketStuff in ticketEntries.items():
        if users[userId].ticket_id == None: users[userId].ticket_id = ticketStuff[0].ticket_id 
        if users[userId].enter_date_time == None: users[userId].enter_date_time = ticketStuff[0].timestamp 
        users[userId].ticketEntries = ticketEntries[userId]
    return users