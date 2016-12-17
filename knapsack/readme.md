# Knapsack problem using depth-first-search

#### Overview
This script finds the maximum value possible when selecting from a list of items with a given weight w and value v, with a capacity constraint based on weight. It answers the age old question 'of all this valuable stuff, what do I put in my knapsack?'. This algorithm uses depth first search to evaluate each item choice and uses a value-estimating heuristic to prune search areas that will not be optimal. The data folder contains possible knapsack configurations, labelled ks_X_Y, where X is the number of items. The algorithm starts to struggle at problems larger than ks_50_0, where a dynamic programming solution seems to be more appropriate.

To run this script use:
python knapsack.py .\data\ks_4_0
in command line, with the data file in the same directory

In the output, the second last line lists the value of the items selected, and the final line shows which items were chosen (1) and which were not (0).


