import heapq
from planogram import get_article_coords, get_article_coords_pickup, get_article
from pprint import pprint
import math
from tickets import TicketEntry
import numpy as np

def transformar_a_problema_lineal(usuari, planogram):

    portaEntrada = TicketEntry("paso-entrada", 0, None,  None) #get_article(planogram, "paso-entrada")
    portaSortida = TicketEntry("paso-salida", 0, None,  None) #get_article(planogram, "paso-salida")

    matriu = []
    for ticketEntrieFirst in usuari.ticketEntries:
        linia = []
        for ticketEntrieSec in usuari.ticketEntries:
            linia.append(shortestPathDistance(ticketEntrieFirst,ticketEntrieSec, planogram))

        linia.append(shortestPathDistance(portaEntrada,ticketEntrieFirst, planogram))
        linia.append(shortestPathDistance(portaSortida,ticketEntrieFirst, planogram))
        matriu.append(linia)
 

    linia = []
    linia2 = []
    for ticketEntrieFirst in usuari.ticketEntries:
        linia.append(shortestPathDistance(portaEntrada,ticketEntrieFirst, planogram))
        linia2.append(shortestPathDistance(portaSortida,ticketEntrieFirst, planogram))

    linia.append(math.inf)
    linia.append(0)
    linia2.append(math.inf)
    linia2.append(math.inf)
    matriu.append(linia)
    matriu.append(linia2)

    return matriu

def shortestPathDistance(entryTicketPickUpFirst, entryTicketPickUpSecond, planogram):
    
    # Coordinates of the start and end points
    x0, y0 = get_article_coords_pickup(planogram, entryTicketPickUpFirst.article_id)
    xf, yf = get_article_coords_pickup(planogram, entryTicketPickUpSecond.article_id)
    #print(x0, y0, xf, yf)
    x0 = int(x0)
    y0 = int(y0)    
    xf = int(xf)
    yf = int(yf)

    if(x0,y0) == (xf, yf):
        return math.inf

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
        #pprint(pq)
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

def find_next_domino(pieces, current_sequence):
    if not pieces:
        return current_sequence

    last_piece = current_sequence[-1]
    for i, piece in enumerate(pieces):
        if piece[0] == last_piece[1]:
            new_sequence = find_next_domino(pieces[:i] + pieces[i+1:], current_sequence + [piece])
            if new_sequence:
                return new_sequence

    return None

def obtenir_assignacions_ordenades(assignacio_optima, matriu=None):
    _, assignacio_optima = assignacio_optima
    ultim_numero = len(assignacio_optima) - 1

    index_to_reverse = next((i for i, elem in enumerate(assignacio_optima) if elem == ultim_numero), ultim_numero)

    assignacio_en_ordre = assignacio_optima[:index_to_reverse + 1][::-1] + assignacio_optima[index_to_reverse + 1:]
    
    #if assignacio_en_ordre:
    #        assignacio_en_ordre.append(assignacio_en_ordre.pop(0))
    assignacio_en_ordre.pop(0)
    assignacio_en_ordre.pop(0)
    return assignacio_en_ordre

    
def optimitzarMatriuCostos(matriu, nombre_files_a_reduir):
    matriu = np.array(matriu)  # Ensure it's a NumPy array
    if np.any(np.isnan(matriu)) or np.any(np.isinf(matriu)):
        raise ValueError("Matrix contains NaN or inf values.")

    merged_indices = []

    while len(matriu) > nombre_files_a_reduir:
        min_distance = float('inf')
        pair_to_merge = None

        for i in range(len(matriu)):
            for j in range(i + 1, len(matriu)):
                # Check if subtraction is valid
                if not np.any(np.isnan(matriu[i])) and not np.any(np.isnan(matriu[j])):
                    distance = np.linalg.norm(matriu[i] - matriu[j])
                    if distance < min_distance:
                        min_distance = distance
                        pair_to_merge = (i, j)

        if pair_to_merge is None:
            raise ValueError("No valid pair found to merge. Check the matrix format and values.")

        i, j = pair_to_merge
        matriu[i] += matriu[j]
        matriu = np.delete(matriu, j, axis=0)
        matriu[:, i] += matriu[:, j]
        matriu = np.delete(matriu, j, axis=1)

        merged_indices.append(pair_to_merge)

    return matriu, merged_indices




def map_to_original_indices(optimized_indices, elements_substituits):

    for indexs in elements_substituits[::-1]:
        x, y = indexs
        ind = optimized_indices.index(x)
        optimized_indices.insert(ind, y)
    return optimized_indices
