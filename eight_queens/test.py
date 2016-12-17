"""
Tests for 8 queens problem.
Run using py.test
"""

import numpy as np

from chessboard import Chessboard

def test_CheckQueens_Queens_ExpectValid():
    board = Chessboard()
    is_valid = board.check_queens()
    assert is_valid

def test_CheckQueens_NoCollisions_ExpectValid():
    board = Chessboard()
    board.rows = np.array([1, 5, 8, 6, 3, 7, 2, 4],dtype=np.int32)
    is_valid = board.check_queens()
    assert is_valid

def test_CheckQueens_ColumnAttack_ExpectInvalid():
    board = Chessboard()
    # both on third column
    board.rows = np.array([3,3,-1,-1,-1,-1,-1,-1],dtype=np.int32)
    is_valid = board.check_queens()
    assert not is_valid

def test_CheckQueens_LeftDiagonalAttack_ExpectInvalid():
    board = Chessboard()
    # queen at (0,3) can left attack queen at (2,1)
    board.rows = np.array([3,-1,1,-1,-1,-1,-1,-1],dtype=np.int32)
    is_valid = board.check_queens()
    assert not is_valid

def test_CheckQueens_RightDiagonalAttack_ExpectInvalid():
    board = Chessboard()
    # queen at (0,3) can right attack queen at (3,6)
    board.rows = np.array([3,-1,-1,6,-1,-1,-1,-1],dtype=np.int32)
    is_valid = board.check_queens()
    assert not is_valid