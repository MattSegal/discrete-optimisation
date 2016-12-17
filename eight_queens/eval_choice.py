#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

from constraint_store import constraint_store

def evaluate_choice( queen, row , row_domain , choice , options , iterations  ):
    solution_found = 0
    
    while True:
        iterations +=1
        
        # assign row to queen from available domain
        options[queen][:]   =   row_domain[queen][:]                # record available options
        choice[queen,0]     =   1                                   # record that a choice has been made (rather than constraint)
        choose              =   choice[queen,1]                     # which queen is picked is influenced by past iterations
        #print 'choice index is ',choose
        #print 'queen is',queen
        row[queen]          =   row_domain[queen][choose]           # assign queen to row
        #row[queen]         =   min(row_domain[queen][:])
        #print options
        #print row_domain
        
        #print 'new row is ',row
        #print 'choice is:\n',choice
                
        # pass info to constraint store
        (feasibility , row_domain)   =   constraint_store( row , row_domain )

        #print 'after constraints, row is ',row
        #print 'constraint store returns feasibility ==',feasibility
        
        if feasibility == 1:
            if sum(row==0)==0: # if a feasible solution is found
                solution_found  =   1    
            return solution_found , row , row_domain , choice, options, iterations # go to calculate next node

        elif feasibility == -1:
            solution_found = -1
           # print "return no solution possible to QUEENS"
            return solution_found , row , row_domain , choice , options , iterations # backtrack to fix bad selection
