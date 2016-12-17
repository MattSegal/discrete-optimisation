#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script implements a constaint-programming solution to the 'Eight Queens Problem'
The problem:
    Place 8 queens on a chessboard such that none can attack each other
The output:
    Prints a list of the 8 chessboard columns 1-8, 
    showing the row position of each queen in a given column
"""


import numpy as np
import copy

from eval_choice import evaluate_choice
from backtrack import backtrack

def check_solution(row):
    pass

def place_queens():
    """
    queens placed column by column using a constraint programming method
    queens placed on 8x8 chessboard so that they cannot attack each other
    """

    # ===== set up =====#
    # board size
    board_width = 8
    # decision variables
    row     =   np.zeros(board_width,dtype=np.int32)
    row_reset = np.array(copy.deepcopy(row))
    
    # row domain
    num_queens		= board_width                                       
    row_list		= np.array([x for x in range(1,num_queens+1)])
    list_broadcast	= np.array([[1] for x in range(num_queens)])
    row_domain		= (row_list * list_broadcast).tolist()
    row_domain_reset	= copy.deepcopy(row_domain)

    # search variables
    choice  =   np.zeros((8,2),dtype=np.int32)  # 1 for chosen, 0 for constraint # second column records choice number /options
    options =   np.zeros((8,1),dtype=np.int32).tolist()
    iterations      =   0 # for debug\

    # find solution
    while True:
	# pick first unchosen queen
        for queen in range(num_queens):
            queen_unspecified = row[queen] == 0
            if queen_unspecified:
                break

	   # evaluate choice
        (solution_found , row , row_domain , choice, options, iterations) = evaluate_choice( queen , row , row_domain , choice , options, iterations )    

        # infeasible arrangement found board_width
        if solution_found == -1:
            (solution_found , choice) = backtrack(choice , options)
            # if backtrack successful, reset search variables
            if solution_found == 0:
                #print "reset search variables"
                search_index = 0
                row = np.array(copy.deepcopy(row_reset))
                row_domain = copy.deepcopy(row_domain_reset)
    
        if solution_found == 1:
            break    
        
    # return solution
    print "solution took ",iterations," iterations"

    print row
    #return row


place_queens()
