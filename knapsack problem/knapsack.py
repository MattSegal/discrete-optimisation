#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Branch and bound solver for the knapsack problem,
uses either BFS (queue) or DFS (stack) to navigate solution tree
uses a value estimating heuristic to prune sub-optimal nodes and reduce the search space

TODO:
    * add memoization to remove unnecessary summing
    * remove unecessary array creation - pre allocate memory
"""

import sys
import time
import numpy as np

from queue import Queue
from stack import Stack

def solve_it(input_text):

    kp = KnapsackProblemData(input_text)

    print 'Number of items   {0}'.format(kp.num_items) 
    print 'Knapsack capacity {0}'.format(kp.capacity)

    start = time.time()
    
    # Pre sort weights and values by density ( value / kg, highest to lowest)
    density         = np.divide(kp.values,kp.weights.astype(float))
    density_order   = np.lexsort((np.zeros(len(density)),density))

    kp.weights      = kp.weights[density_order[::-1]]
    kp.values       = kp.values[density_order[::-1]]

    # Begin branch and bound tree search
    best_value    = 0 

    stack = Stack() # Set to Stack for DFS or Queue for BFS
    stack.push([0]) # Initial choice of 'don't take the first item'
    stack.push([1]) # Initial choice of 'take the first item'

    # Loop until all branches have been explored or pruned
    while len(stack) > 0:
        choice = stack.pop()

        num_chosen = len(choice)

        # TODO: Try memoizing these values and pushing them onto the stack
        current_weight = np.sum(np.multiply(kp.weights[0:num_chosen],np.array(choice)))
        current_value  = np.sum(np.multiply(kp.values[0:num_chosen],np.array(choice)))
        
        if current_weight > kp.capacity:
            # Prune the node, search elsewhere
            continue

        node_is_leaf = num_chosen == kp.num_items
        
        if node_is_leaf:
            current_value_is_best = current_value > best_value

            if current_value_is_best:
                best_value  = current_value 
                best_weight = current_weight  
                best_choice = choice
        else:
            # Estimate upper bound for knapsack's value given current choices
            estimated_value = estimate_value(kp,choice,current_weight,current_value)
            estimated_value_is_suboptimal = estimated_value < best_value
            
            if estimated_value_is_suboptimal:
                # Prune the node, search elsewhere
                continue
        
            # Keep exploring the tree from this node
            stack.push(choice + [0]) # Try not choosing next item
            stack.push(choice + [1]) # Try choosing next item

    end = time.time()
    print "Time taken (s) = ",int((end-start))

    optimal = 1 # 1 if solution seems optimal
    # Prepare the solution in the required output format
    output_data = "{0} {1}\n{2}".format(best_value, optimal, best_choice)
    
    return output_data

# =============================================================================== #

def estimate_value(kp,choice,current_weight,current_value):
    """
    Calculate upper bound on value to be obtained for a given choice.
    Select each item greedily by value density - already sorted highest to lowest
    """

    num_chosen    = len(choice)
    num_to_choose = len(kp.values)

    mass_knapsack  = current_weight
    assert mass_knapsack <= kp.capacity
    value_knapsack = current_value

    for item_idx in range(num_chosen,num_to_choose):

        # Pick items using value greed, with a fracton of the last item
        item_weight = kp.weights[item_idx]
        item_value  = kp.values[item_idx]
        new_mass = mass_knapsack + item_weight

        if new_mass <= kp.capacity:
            # Keep adding items
            value_knapsack += item_value
            mass_knapsack  = new_mass

        else:
            # Add a fraction of the last item to get upper bound
            remaining_mass   = kp.capacity - mass_knapsack
            item_fraction    = remaining_mass / float(item_weight)
            value_knapsack  += item_value  * item_fraction
            mass_knapsack   += item_weight * item_fraction
            break

    return value_knapsack

# =============================================================================== #

class KnapsackProblemData:
    def __init__(self,input_text):
        # eg, input_text = "4 11\n8 4\n10 5\n15 8\n4 3\n"

        lines = input_text.strip('\n').split('\n')                 
        (self.num_items,self.capacity) = (int(num) for num in lines[0].split())

        values = []
        weights = []
        
        for line in lines[1:]:
            (value,weight) = (int(num) for num in line.split())
            values.append(value)
            weights.append(weight)

        self.values = np.array(values)
        self.weights = np.array(weights)

# =============================================================================== #

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1].strip()
        with open(filename, 'r') as f:
            input_text = ''.join(f.readlines())
        print solve_it(input_text)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python knapsack.py ./data/ks_4_0)'


