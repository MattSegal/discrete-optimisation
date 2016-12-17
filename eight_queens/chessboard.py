import numpy as np

class Chessboard(object):
    """ Chessboard for the 8 Queens problem
    """
    BOARD_WIDTH = 8
    EMPTY       = -1

    def __init__(self):
        # Array of rows on which the queen may be placed
        # Placement is indicated by the column number in the row
        self.rows = np.ones(self.BOARD_WIDTH,dtype=np.int32) * self.EMPTY

    def place_queen(self,row,col):
        """ Place a Queen on the chessboard
        """
        assert 0 <= col <= self.BOARD_WIDTH
        self.rows[row] = col

    def remove_queen(self,row):
        """ Remove a placed Queen from a given column on the chessboard
        """
        self.rows[row] = self.EMPTY

    def check_queens(self):
        """ Verify that no placed Queen can attack any other placed Queen
        """
        for attacker_row_idx in range(self.BOARD_WIDTH - 1):
            attacker_col = self.rows[attacker_row_idx]

            if attacker_col == self.EMPTY:
                continue

            for victim_row_idx in range(attacker_row_idx+1,self.BOARD_WIDTH):
                victim_col = self.rows[victim_row_idx]

                # Two queens in the same row are not allowed by the rows array.
                is_col_attack = victim_col == attacker_col

                # Two queens on the same diagonal cannot attack each other
                row_diff = victim_row_idx - attacker_row_idx
                is_left_row_attack = victim_col + row_diff == attacker_col
                is_right_row_attack = victim_col + row_diff == attacker_col

                if is_col_attack or is_right_row_attack or is_left_row_attack:
                    return False

        return True