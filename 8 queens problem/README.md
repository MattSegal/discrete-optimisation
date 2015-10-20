# 8 Queens

#### Overview
This script finds a way to position 8 queens on a chessboard with none of them able to attack any other queen.
It uses a constaint solver to remove all possible choices the violate the problem's constrains - reducing the size of the search space.

To run this script use:
python queens.py
in command line.

#### Possible Future Work
Remove the backtracking search style and instead use a more efficient form of graph based search to navigate the tree. Ideally remove uneccessary variables used to search the problem-space - this would make the code much easier to read. 

Make it possible for a user to select the placement of the first queen.

