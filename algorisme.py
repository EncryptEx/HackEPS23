import numpy as np
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

