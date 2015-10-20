import numpy as np

def backtrack(choice,options):
    #print "\n===== infeasible solution found, try backtrack =====\n"
    #print 'choice vector:\n ',choice
    #print 'option list:\n ',options
    
    while True:
    
        choice_record = choice[:,0]
        chosen_options_list = choice[:,1]

        choice_column  = np.max(np.where(choice_record>0))  # index (row) of the most recent choice
        option_chosen = chosen_options_list[choice_column]
    
        num_options = len(options[choice_column][:])
        more_options_possible = num_options > option_chosen + 1
    
        if more_options_possible:
            # try next option
            choice[choice_column,0] = 0
            choice[choice_column,1] = option_chosen + 1
            #print 'more options available for column',choice_column,'try choosing option ',option_chosen+1
            solution_found = 0
            break
        else:
            # reset current, maxed out choice
            choice[choice_column,0] = 0
            choice[choice_column,1] = 0
            # repeat loop to try previous choice
            #print 'no choices left for row ',choice_column
            # ================ FIX THIS ============= #
            no_choices_left = False#np.sum(choice[:,1]) == 0
        if no_choices_left:
            #print "all choices have been tried, no solution possible"
            solution_found = 1
            break
    #print 'output choice vector: \n',choice
    #print 'output solution found =',solution_found

    return solution_found, choice
