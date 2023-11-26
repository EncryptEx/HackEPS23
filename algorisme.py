import numpy as np
import itertools
from scipy.optimize import linear_sum_assignment

def minimum_assignment(matrix):
    # Convert the matrix to a numpy array for compatibility with scipy
    matrix = np.array(matrix)
    
    # Apply the Hungarian algorithm
    row_ind, col_ind = linear_sum_assignment(matrix)
    
    # Return the optimal assignment and its total cost
    optimal_cost = matrix[row_ind, col_ind].sum()
    optimal_assignment = list(zip(row_ind, col_ind))

    return optimal_assignment, optimal_cost




import itertools

def algorisme_ineficient(dists):
    n = len(dists)
    C = {}
    
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            for k in subset:
                prev = bits & ~(1 << k)
                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    bits = (2**n - 1) - 1
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)
    
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    path.append(0)
    
    return opt, list(reversed(path))


def tsp(dists):
    n = len(dists)
    C = {}
    
    # Initialize starting node paths
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    # Build up all combinations of paths
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find the cheapest path to this subset
            for k in subset:
                prev = bits & ~(1 << k)
                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    if (prev, m) in C:
                        res.append((C[(prev, m)][0] + dists[m][k], m))
                if res:
                    C[(bits, k)] = min(res)

    # Final path
    bits = (2**n - 1) - 1
    res = []
    for k in range(1, n):
        if (bits, k) in C:
            res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    # Reconstruct path
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    path.append(0)
    
    return opt, list(reversed(path))



def tsp_brute_force(cost_matrix):
    # Number of cities
    n = len(cost_matrix)
    
    # Generate all possible tours
    tours = itertools.permutations(range(n))
    
    # Initialize minimum cost and path
    min_cost = float('inf')
    min_path = None
    
    # Iterate over all tours and calculate the total cost
    for tour in tours:
        current_cost = 0
        for i in range(n - 1):
            current_cost += cost_matrix[tour[i]][tour[i + 1]]
        # Add cost for returning to the start city
        current_cost += cost_matrix[tour[-1]][tour[0]]
        
        # Update min cost and path if current cost is lower
        if current_cost < min_cost:
            min_cost = current_cost
            min_path = tour
            
    return min_path, min_cost

