# Discrete Optimisation

#### Overview
When starting to learn python I first tackled the Coursera course Discrete Optimsation, which teaches heuristics for solving NP-hard combinatorial problems. 

At the time I didn't know much about algorithms, and I came up with some very strange, quirky solutions. In these challenges I learned the value of a good algorithm - my early code took minutes to solve a problem which would later take seconds. 

If I were to re-do these problems now I would like to try to apply what I've learned from Algorithms to make them run faster, and also generally refactor them to be more readable and elegant. I hope to find the time to come back and finish the course and beat my current running times.

## Shower Thought
The knapsack problem can be solved very quickly with a dynamic programming solution, but the problem is that the solution array takes up a prohibitive amount of memory for larger problems. It is possible to find the optimal solution by only storing the last valid answer, but then it is hard to backtrack and find the items required to obtain the optimal solutions. Recently I realized that backtracking might be possible, and might not slow the algorithm too much. 
