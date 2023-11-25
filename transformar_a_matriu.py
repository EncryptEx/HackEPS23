import heapq
from planogram import get_article_coords

def transformar_a_problema_lineal(usuari, planogram):
    matriu = []
    for ticketEntrieFirst in usuari.ticketEntries:
        linia = []
        for ticketEntrieSec in usuari.ticketEntries:
            linia.append(shortestPathDistance(ticketEntrieFirst,ticketEntrieSec, planogram))
        matriu.append(linia)
    
    return matriu


def shortestPathDistance(entryTicketPickUpFirst, entryTicketPickUpSecond, planogram): #FIXME FER QUE NO RETORNI NI EL HEAD NI EL FINAL
    
    # Coordinates of the start and end points
    x0, y0 = get_article_coords(planogram, entryTicketPickUpFirst.article_id)
    xf, yf = get_article_coords(planogram, entryTicketPickUpSecond.article_id)

    x0 = int(x0)
    y0 = int(y0)    
    xf = int(xf)
    yf = int(yf)

    maxX = len(planogram)
    maxY = len(planogram.get('1'))

    # Priority queue for Dijkstra's algorithm
    pq = []
    heapq.heappush(pq, (0, (x0, y0)))  # (distance, (x, y))
    #fix me , mirar que no estigui out of bounds

    # A set to keep track of visited cells
    visited = set()

    # Movement vectors for up, down, left, right
    movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while pq:
        dist, (x, y) = heapq.heappop(pq)

        # If the cell is already visited, skip it
        if (x, y) in visited:
            continue

        visited.add((x, y))

        # Check if we've reached the destination
        if (x, y) == (xf, yf):
            return dist

        # Check adjacent cells
        for dx, dy in movements:
            nx, ny = x + dx, y + dy
            if nx >= maxX or ny >= maxY:
                continue
            
            next_cell = planogram.get(str(nx), {}).get(str(ny))

            # Continue only if the cell is a 'paso' and not visited
            if next_cell and next_cell.description == 'paso' and (nx, ny) not in visited:
                heapq.heappush(pq, (dist + 1, (nx, ny)))


    return -1

def shortestPath(entryTicketPickUpFirst, entryTicketPickUpSecond, planogram):
    # Coordinates of the start and end points
    x0, y0 = get_article_coords(planogram, entryTicketPickUpFirst.article_id)
    xf, yf = get_article_coords(planogram, entryTicketPickUpSecond.article_id)

    maxX = len(planogram)
    maxY = len(planogram.get('1'))
    # Priority queue for Dijkstra's algorithm
    pq = []
    heapq.heappush(pq, (0, (x0, y0)))  # (distance, (x, y))

    # A set to keep track of visited cells
    visited = set()

    # Dictionary to store the predecessors of each node
    predecessors = {}

    # Movement vectors for up, down, left, right
    movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while pq:
        dist, (x, y) = heapq.heappop(pq)

        # If the cell is already visited, skip it
        if (x, y) in visited:
            continue
        
        visited.add((x, y))

        # Check if we've reached the destination
        if (x, y) == (xf, yf):
            return reconstruct_path(predecessors, (x0, y0), (xf, yf))

        # Check adjacent cells
        for dx, dy in movements:
            nx, ny = x + dx, y + dy
            if nx >= maxX or ny >= maxY:
                continue
            next_cell = planogram.get(str(nx), {}).get(str(ny))

            # Continue only if the cell is a 'paso' and not visited
            if next_cell and next_cell.description == 'paso' and (nx, ny) not in visited:
                predecessors[(nx, ny)] = (x, y)
                heapq.heappush(pq, (dist + 1, (nx, ny)))

    return []

def reconstruct_path(predecessors, start, end):
    path = [end]
    while path[-1] != start:
        path.append(predecessors[path[-1]])
    path.reverse()
    return path

def obtenir_assignacions_ordenades(assignacio_optima, matriu=None):
    # If only the row indices are needed
    assignacions_ordenades = [row for row, _ in assignacio_optima]

    # If the actual values from the matrix are needed
    if matriu is not None:
        assignacions_ordenades = [matriu[row][col] for row, col in assignacio_optima]

    return assignacions_ordenades