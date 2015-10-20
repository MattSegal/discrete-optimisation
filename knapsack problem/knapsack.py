#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Branch and bound solver for the knapsack problem,
uses either BFS (queue) or DFS (stack) to navigate solution tree
uses a value estimating heuristic to prune sub-optimal nodes and reduce the search space
"""

import numpy as np  # NumericalPython for array functions
import time         # for timing optimisation process

from knapsack_data_structures import Queue
from knapsack_data_structures import Stack


# UNIT TESTS
def test_parse_input():
    input_data = "4 11\n8 4\n10 5\n15 8\n4 3\n"
    (value,weight,num_items,capacity) = parse_input(input_data)
    assert num_items == 4
    assert capacity == 11
    # value and weight sorted by denisty
    assert (value == np.array([10,8,15,4])).all()
    assert (weight == np.array([5,4,8,3])).all()
    
    input_data = "3 15\n1 1\n1 2\n1 3\n"
    (value,weight,num_items,capacity) = parse_input(input_data)
    assert num_items == 3
    assert capacity == 15
    # value and weight sorted by denisty    
    assert (value == np.array([1,1,1])).all()
    assert (weight == np.array([1,2,3])).all()
    

    input_data = "3 20\n1 1\n2 1\n3 1\n"
    (value,weight,num_items,capacity) = parse_input(input_data)
    assert num_items == 3
    assert capacity == 20
    # value and weight sorted by denisty    
    assert (value == np.array([3,2,1])).all()
    assert (weight == np.array([1,1,1])).all()
    

def test_estimate_value():
    input_data = "4 11\n8 4\n10 5\n15 8\n4 3\n"
    (value,weight,num_items,capacity) = parse_input(input_data)
    choice = [1,1,0]
    # value vector  [ 10 8  15 4 ]
    # weight vector [ 5  4  8  3 ]
    # choice gets weight 5+4 = 9 with remaining capacity 2
    # choice gets value 10+8 = 18
    # we can take 2/3 of item 4, giving us added value of (2/3)*4 = 2.67
    # estimated value == 20.67
    estimated_value = estimate_value(capacity,value,weight,choice)
    assert choice == [1,1,0] # choice should not mutate
    assert estimated_value == 18 + (2*4)/float(3)

    choice = [1,0]
    # value vector  [ 10 8  15 4 ]
    # weight vector [ 5  4  8  3 ]
    # choice gets weight 5 = 5 with remaining capacity 6
    # choice gets value 10 = 10
    # we can take 6/8 of item 3, giving us added value of (3/4)*15 = 11.25
    # estimated value == 21.25
    estimated_value = estimate_value(capacity,value,weight,choice)
    assert choice == [1,0] # choice should not mutate
    assert estimated_value == 21.25

    choice = [0,0]
    # value vector  [ 10 8  15 4 ]
    # weight vector [ 5  4  8  3 ]
    # choice gets weight 0 with remaining capacity 11
    # choice gets value 0
    # we take all of item 3
    #	value = 15
    #	weight = 8
    # we can take all of item 4, giving us added value of 4
    # estimated value == 19
    estimated_value = estimate_value(capacity,value,weight,choice)
    assert choice == [0,0] # choice should not mutate
    assert estimated_value == 19


def test_solve_it():
    # 4 item problem
    input_data = "4 11\n8 4\n10 5\n15 8\n4 3\n"
    
    best_value = 19.0
    optimal = 1
    best_choice = [0,0,1,1]
    output_data = str(best_value) + ' ' + str(optimal) + '\n'
    output_data += str(best_choice)
    
    result = solve_it(input_data)
    assert result == output_data

    # 19 item problem
    input_data = "19 31181\n1945 4990\n321 1142\n2945 7390\n4136 10372\n1107 3114\n1022 2744\n1101 3102\n2890 7280\n962 2624\n1060 3020\n805 2310\n689 2078\n1513 3926\n3878 9656\n13504 32708\n1865 4830\n667 2034\n1833 4766\n16553 40006"

    best_value = 12248.0
    optimal = 1
    best_choice = [0,0,1,0,1,1,0,0,1,0,1,0,0,0,0,0,0,0,0]
    output_data = str(best_value) + ' ' + str(optimal) + '\n'
    output_data += str(best_choice)
    result = solve_it(input_data)
    assert result == output_data

# =============================================================================== #

def solve_it(input_data):
    
    (value,weight,num_items,capacity) = parse_input(input_data)

    start = time.time()
    
    print 'number of items = %d' % num_items 
    print 'capacity = %d' % capacity

    best_value    = 0       
    best_weight  = None
    best_choice  = None

    # ===== Branch and Bound Search ===== #

    stack = Stack() # set to Stack() for DFS or Queue for BFS
    stack.push([0])
    stack.push([1])

    # loop until all branches explored/pruned - when there are no items left in stack
    while len(stack) > 0:
	choice = stack.pop()

	current_weight = np.sum(np.multiply(weight[0:len(choice)],np.array(choice)))
	over_capacity = current_weight > capacity
	
	if over_capacity:
	    # prune node, search elsewhere
            continue
        else:
            node_is_leaf = len(choice) == num_items
            if node_is_leaf:
		current_value = np.sum(np.multiply(value,np.array(choice)))
                new_best_value = current_value > best_value
                if new_best_value:
		    best_value = current_value 
                    best_weight = current_weight  
                    best_choice = choice
            else:
                # estimate upper bound for knapsack value
                estimated_value = estimate_value(capacity,value,weight,choice);
                if estimated_value < best_value:
		    # prune node, search elsewhere
		    continue
                else:
		    # keep exploring down the tree from the node using DFS or BFS
		    choice.append(0)
		    stack.push(choice[:])
		    choice[-1] = 1
		    stack.push(choice[:])
			
    # ===== Search Complete, Return Values ===== #

    end = time.time()
    print "Time taken (s) = ",int((end-start))

    optimal = 1 # 1 if solution seems optimal
    # prepare the solution in the specified output format
    output_data = str(best_value) + ' ' + str(optimal) + '\n'
    output_data += str(best_choice)
    
    return output_data

# =============================================================================== #

def parse_input(input_data):
    """
    returns input data in a more easy to process format
    """
    lines = input_data.split('\n')                 
    firstLine = lines[0].split()    
    num_items = int(firstLine[0])           
    capacity = int(firstLine[1])          

    value = []
    weight = []
    
    for item in range(1, num_items+1):	# for i = [1 to n+1]
        line = lines[item]              # line = 'vi wi'
        parts = line.split()            # parts = ['vi','wi']
        value.append(int(parts[0]))     # value vector [ v0 .... v(n-1) ]
        weight.append(int(parts[1]))    # weight vector [ w0 .... w(n-1) ]

    value = np.array(value)
    weight = np.array(weight)

    # calculate density
    density = np.divide(value.astype(float),weight.astype(float)) # density vector
    # sort from lowest to highest density - gives an np.array of indices of items sorted by density
    density_order = np.lexsort((np.zeros(len(density)),density))

    value_sorted = np.zeros(num_items)
    weight_sorted = np.zeros(num_items)

    # copy value and weight list into numpy array in density sorted order (highest to lowest)
    sorted_index = 0
    for index in reversed(density_order):
	value_sorted[sorted_index] = value[index]
	weight_sorted[sorted_index] = weight[index]
	sorted_index += 1

    return (value_sorted,weight_sorted,num_items,capacity)    

# =============================================================================== #

def estimate_value(capacity,value,weight,choice):
    """
    select each item by by value density - already sorted
    select fraction of last available item using linear relaxation
    CONSIDER:
	you can trade time for memory by storing past results for this function
	and re using them in future calls - could use a stack in parallel to choice stack
	not 100% on how to implement, but this may help with a likely bottleneck
    """
    choice = choice[:] # so choice doesn't get mutated
    choices_remaining = len(value) - len(choice)
    for undecided_choice in range(choices_remaining):
	choice.append(1)    # take the item for all undecided choices

    # pick items using value greed, with a fracton of the last item
    mass_knap = 0	# mass of knapsack
    value_knap = 0	# sum of value in knapsack
    for item in range(len(choice)):
        if choice[item] == 1:
            if (mass_knap + weight[item]) <= capacity:
                value_knap += value[item]
                mass_knap += weight[item]
            elif mass_knap < capacity:
		item_fraction = (capacity-mass_knap)/float(weight[item])
                value_knap += value[item]*item_fraction
                mass_knap += weight[item]*item_fraction
            elif mass_knap >= capacity:
                break

    return value_knap

# =============================================================================== #

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:                                   # opens data file if data file is given as the first argument eg. python solver.py ./data/ks_4_0
        file_location = sys.argv[1].strip()                 # removes whitespace
        input_data_file = open(file_location, 'r')          # opens input data file
        input_data = ''.join(input_data_file.readlines())   # stores input data as a string
        input_data_file.close()                             # closes input data file
        print solve_it(input_data)                          # prints result of solve it, with input data as the function inputs
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'


