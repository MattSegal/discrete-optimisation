import numpy as np
  
def constraint_store( row , row_domain ):
    while True:
        repeat_constraint_propagation = False
        #print 'row passed to constraint store ',row
        #print 'domain ',row_domain
        
        # ===== feasibility check ===== #
        feasibility = 1
        # iterate through all combinations of queens
        for i in range(8):
            for j in range(8):
                if i == j:
                    break       
        
                both_queens_placed  =   row[i] * row[j] > 0
                one_queen_placed    =   row[i] + row[j] > 0
        
                if both_queens_placed:
                    # constraint #1 - no two placed queens may be able to attack each other
                    # constraint deletes offending rows, with preference to delete j > i
                    (row_domain,feasibility) = constraint1(i,j,row,row_domain)

                elif one_queen_placed and both_queens_placed == False:
                    # constraint #2 - least one value in row domain of unspecified queen that cannot attack the specified queen
                    feasibility = constraint2(i,j,row,row_domain)

                elif one_queen_placed == False:
                    # constraint #3 - two unspecified rows with only one value in each domain must not be able to attack each other
                    feasibility = constraint3(i,j,row,row_domain)
            
        if feasibility == 1:
            
            # ===== propagate constraints ===== #
            row_domain = propagate_constraints(row,row_domain)
                
        
            # ===== choose constrained queens ===== #
            # if any queen is unassigned and has only one value left in domain then choose that value and repeat constraint propagation
            for i in range(8):
                queen_not_placed    =   row[i] == 0
                one_value_left      =   len(row_domain[i][:]) == 1
                
                if queen_not_placed and one_value_left:
                    #print '\n===== Auto Assign Value ====='
                    #print 'column ',i,' has one value left in domain ',row_domain[i][:]
                    row[i] = row_domain[i][0]
                    repeat_constraint_propagation = True


        empty_domain = len(min(row_domain,key=len)) == 0
        if empty_domain:
                    feasibility = -1
                    #print "infeasible empty domain detected"

        # ===== exit constraint store ===== #
        if repeat_constraint_propagation == False or feasibility == 0 or feasibility == -1:
            break
        # end of while loop
        
    #print 'final domain ',row_domain
    #print 'final feasibility',feasibility

    return [feasibility, row_domain]

# =============================================================================== #

def remove_row(row_domain,row,queen):
    # delete row value from the the domain of queen
    #print 'remove row',row,' from column',queen,' with domain \n',row_domain
    row_remove_index = row_domain[queen][:].index(row)
    del row_domain[queen][row_remove_index]
    return row_domain

# =============================================================================== #

def constraint1(i,j,row,row_domain):
    # constraint #1 - no two placed queens(i,j) may be able to attack each other
    feasibility         =   1
    same_row            =   row[i] == row[j]
    same_up_diag        =   row[i] - i  == row[j] - j
    same_down_diag      =   row[i] + i  == row[j] + j
    can_attack          =   same_row or same_up_diag or same_down_diag
                    
    if can_attack:
        feasibility = 0
        
        # remove offending element from domain so that next iteration doesn't make same mistake          
        # preferentially remove elements from column j - because of bottum up backtrack method
        q = j
        one_row_in_domain_j = len(row_domain[j][:]) == 1
        if one_row_in_domain_j:                                             
            q = i
            one_row_in_domain_i = len(row_domain[i][:]) == 1
            if one_row_in_domain_i:                                             
                #print "error - solver tried to remove last color",row_domain[q][:]," from domain of queen ",q    # debug
                feasibility = -1
        #print 'rows are ',row
        #print 'queen j in (',row[j],',',j,')'
        #print 'queen i in (',row[i],',',i,')'
        #print 'row attack: ',same_row
        #print 'up diag attack: ',same_up_diag
        #print 'down diag attack: ',same_down_diag
        #print 'remove row ',row[q],' from column ',q,' with domain:'
        #print row_domain[q]
        #print " "
        if feasibility == 0:
            row_domain = remove_row(row_domain,row[q],q)

    return(row_domain,feasibility)

# =============================================================================== #

def constraint2(i,j,row,row_domain):
    # find which queen, i or j is the specified queen, and which is unspecified
    # count at least one value in row domain of unspecified queen that cannot attack the specified queen
    feasibility = 1
                
    if row[i] == 0:
        unspec_queen        =   i
        spec_queen          =   j
        spec_queen_row      =   row[j]
    else:
        unspec_queen        =   j
        spec_queen          =   i
        spec_queen_row      =   row[i]
            
    unspec_row_domain       =   np.array(row_domain[unspec_queen][:])
                
    diff_row        =   np.sum(unspec_row_domain != spec_queen_row) > 0
    diff_up_diag    =   np.sum(unspec_row_domain - unspec_queen != spec_queen_row - spec_queen) > 0
    diff_down_diag  =   np.sum(unspec_row_domain + unspec_queen != spec_queen_row + spec_queen) > 0
    feasible_value  =   diff_row * diff_up_diag * diff_down_diag
                    
    if feasible_value == False:
        feasibility = -1

    return feasibility 

# =============================================================================== #

def constraint3(i,j,row,row_domain):
    # two unspecified rows with only one value in each domain must not be able to attack each other
    feasibility = 1
    one_value_left_i      =   len(row_domain[i][:]) == 1
    one_value_left_j      =   len(row_domain[j][:]) == 1
    
    if one_value_left_i and one_value_left_j:

        row_i                   =   row_domain[i][0]
        row_j                   =   row_domain[j][0]
 
        diff_row        =   row_i       != row_j
        diff_up_diag    =   row_i - i   != row_j - j
        diff_down_diag  =   row_i + i   != row_j + j
        feasible_value  =   diff_row * diff_up_diag * diff_down_diag
                        
        if feasible_value == False:
            feasibility = -1

    return feasibility
    
# =============================================================================== #

def propagate_constraints(row,row_domain):
    # remove chosen row and diagonals from other queen domains
    # iterate through all combinations of queens from right to left on chessboard
    # currently iterates through already placed queens, inefficient
    for i in range(8):
        for j in range(8):
                    
            one_queen_placed    =   row[i] + row[j] > 0
                    
            if i == j or one_queen_placed == False:
                continue

                    
            if row[i] == 0:
                unspec_queen        =   i
                spec_queen          =   j
            else:
                unspec_queen        =   j
                spec_queen          =   i


            bad_row         =   row[spec_queen]                                 # queen in column j cant be in same row as queen in i
            bad_up_diag     =   row[spec_queen] + (unspec_queen-spec_queen)     # queen in column j cant be in same up diagonal as queen in i
            bad_down_diag   =   row[spec_queen] - (unspec_queen-spec_queen)     # queen in column j cant be in same down diagonal as queen in i
                
            bad_row_in_domain       =   bad_row in row_domain[unspec_queen][:]
            bad_up_diag_in_domain   =   bad_up_diag in row_domain[unspec_queen][:]
            bad_down_diag_in_domain =   bad_down_diag in row_domain[unspec_queen][:]
                
            if bad_row_in_domain:
                # delete bad row value the domain of queen j
                row_domain = remove_row(row_domain,bad_row,unspec_queen)
                #print 'remove row ',bad_row,' from column ',unspec_queen+1,' b/c row attack'

            if bad_up_diag_in_domain:
                # delete bad row value the domain of queen j
                row_domain = remove_row(row_domain,bad_up_diag,unspec_queen)
                #print 'remove row ',bad_up_diag,' from column ',unspec_queen+1,' b/c up diag attack'

            if bad_down_diag_in_domain:
                # delete bad row value the domain of queen j
                row_domain = remove_row(row_domain,bad_down_diag,unspec_queen)
                #print 'remove row ',bad_down_diag,' from column ',unspec_queen+1,' b/c up diag attack'

    return row_domain

# =============================================================================== #
