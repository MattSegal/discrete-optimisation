"""
Run using 
    py.test unit_tests.py
"""

import numpy as np
from knapsack import estimate_value, solve_it, KnapsackProblemData


def test_parse_input_1():
    input_text = "4 11\n8 4\n10 5\n15 8\n4 3\n"
    kp = KnapsackProblemData(input_text)
    assert kp.num_items == 4
    assert kp.capacity == 11
    assert (kp.values == np.array([8,10,15,4])).all()
    assert (kp.weights == np.array([4,5,8,3])).all()

def test_parse_input_2():
    input_text = "3 15\n1 1\n1 2\n1 3\n"
    kp = KnapsackProblemData(input_text)
    assert kp.num_items == 3
    assert kp.capacity == 15    
    assert (kp.values == np.array([1,1,1])).all()
    assert (kp.weights == np.array([1,2,3])).all()
    

def test_parse_input_3():
    input_text = "3 20\n1 1\n2 1\n3 1\n"
    kp = KnapsackProblemData(input_text)
    assert kp.num_items == 3
    assert kp.capacity == 20    
    assert (kp.values == np.array([1,2,3])).all()
    assert (kp.weights == np.array([1,1,1])).all()
    
def test_estimate_value_1():
    input_text = "4 11\n8 4\n10 5\n15 8\n4 3\n"
    choice = [1,1,0]
    kp = KnapsackProblemData(input_text)
    num_chosen = len(choice)
    current_weight = np.sum(np.multiply(kp.weights[0:num_chosen],np.array(choice)))
    current_value  = np.sum(np.multiply(kp.values[0:num_chosen],np.array(choice)))
    # value vector  [ 10 8  15 4 ]
    # weight vector [ 5  4  8  3 ]
    # choice gets weight 5+4 = 9 with remaining capacity 2
    # choice gets value 10+8 = 18
    # we can take 2/3 of item 4, giving us added value of (2/3)*4 = 2.67
    # estimated value == 20.67
    estimated_value = estimate_value(kp,choice,current_weight,current_value)
    assert choice == [1,1,0] # choice should not mutate
    assert estimated_value == 18 + (2*4)/float(3)

def test_estimate_value_2():
    input_text = "4 11\n8 4\n10 5\n15 8\n4 3\n"
    choice = [0,0]
    kp = KnapsackProblemData(input_text)
    num_chosen = len(choice)
    current_weight = np.sum(np.multiply(kp.weights[0:num_chosen],np.array(choice)))
    current_value  = np.sum(np.multiply(kp.values[0:num_chosen],np.array(choice)))
    # value vector  [ 10 8  15 4 ]
    # weight vector [ 5  4  8  3 ]
    # choice gets weight 0 with remaining capacity 11
    # choice gets value 0
    # we take all of item 3
    #	value = 15
    #	weight = 8
    # we can take all of item 4, giving us added value of 4
    # estimated value == 19
    estimated_value = estimate_value(kp,choice,current_weight,current_value)
    assert choice == [0,0] # choice should not mutate
    assert estimated_value == 19

def test_solve_it_4_items():
    # 4 item problem
    input_text = "4 11\n8 4\n10 5\n15 8\n4 3\n"
    
    best_value = 19
    optimal = 1
    best_choice = [0,0,1,1]
    output_data = str(best_value) + ' ' + str(optimal) + '\n'
    output_data += str(best_choice)
    
    result = solve_it(input_text)
    assert result == output_data

def test_solve_it_19_items():
    # 19 item problem
    input_text = "19 31181\n1945 4990\n321 1142\n2945 7390\n4136 10372\n1107 3114\n1022 2744\n1101 3102\n2890 7280\n962 2624\n1060 3020\n805 2310\n689 2078\n1513 3926\n3878 9656\n13504 32708\n1865 4830\n667 2034\n1833 4766\n16553 40006"

    best_value = 12248
    optimal = 1
    best_choice = [0,0,1,0,1,1,0,0,1,0,1,0,0,0,0,0,0,0,0]
    output_data = str(best_value) + ' ' + str(optimal) + '\n'
    output_data += str(best_choice)
    result = solve_it(input_text)
    assert result == output_data
