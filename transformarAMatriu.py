import heapq

def transformarAProblemaLineal(usuari, planogram):
    matriu = []
    for elementToPickUpFirst in usuari.elementsToPickUp:
        linia = []
        for elementToPickUpSecond in usuari.elementsToPickUp:
            linia.append(shortestPath(elementToPickUpFirst,elementToPickUpSecond, planogram))
        matriu.append(linia)
    
    return matriu


def shortestPath(elementToPickUpFirst, elementToPickUpSecond, planogram):
    # Coordinates of the start and end points
    x0, y0 = elementToPickUpFirst.getCoords()
    xf, yf = elementToPickUpSecond.getCoords()

    # Priority queue for Dijkstra's algorithm
    pq = []
    heapq.heappush(pq, (0, (x0, y0)))  # (distance, (x, y))

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
            next_cell = planogram.get(str(nx), {}).get(str(ny))

            # Continue only if the cell is a 'paso' and not visited
            if next_cell and next_cell.description == 'paso' and (nx, ny) not in visited:
                heapq.heappush(pq, (dist + 1, (nx, ny)))


    return -1
