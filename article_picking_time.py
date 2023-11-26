from utils import read_csv_file


# DOC: ./input/hackathon_article_picking_time.csv
# returns a dictionary with article_id as key and a subdict as value
# This subdict cointains article_name and timings as keys
# Timings contains an array of 5 timings
def get_article_picking_time(file_name):
    article_picking_time = {}
    csv_file = read_csv_file(file_name)
    count = 0
    for row in csv_file:
        if(count != 0):
            elements = row[0].split(';')
            article_picking_time[elements[0]] = {'article_name': elements[1], 'timings': elements[2:]}
        count+=1
    return article_picking_time

def search_article_picking_time(product_offsets, article_id):
    for k,v in product_offsets.items():
        if(k == article_id):
            return v['timings']