"""
The minimax algorithm.

Copyright (c) 2022 falwat, under MIT License.
"""
import numpy as np
from gobang_cli import show_board
from agent import Agent
from utils import Piece, check, check_value
from numba import njit
from numba.typed import List

@njit
def indexes_union(board: np.ndarray, indexes: list, 
                    row: int, col: int, span: int = 1):
    row_lb = max(0, row - span)
    row_ub = min(board.shape[0], row + span + 1)
    col_lb = max(0, col - span)
    col_ub = min(board.shape[1], col + span + 1)
    section = board[row_lb:row_ub, col_lb:col_ub]
    row_r, col_r = np.nonzero(section==0)
    new_idxs = (row_r + row_lb) * board.shape[1] + (col_r + col_lb)
    union_indexes = indexes[:]
    for i in new_idxs:
        if i not in indexes:
            union_indexes.append(i)
    for i in range(len(union_indexes)):
        if union_indexes[i] == row * board.shape[1]  + col:
            del union_indexes[i]
            break
    return union_indexes

@njit
def indexes_union_init(board: np.ndarray, 
                    row: int, col: int, span: int = 1):
    row_lb = max(0, row - span)
    row_ub = min(board.shape[0], row + span + 1)
    col_lb = max(0, col - span)
    col_ub = min(board.shape[1], col + span + 1)
    section = board[row_lb:row_ub, col_lb:col_ub]
    row_r, col_r = np.nonzero(section==0)
    new_idxs = (row_r + row_lb) * board.shape[1] + (col_r + col_lb)
    union_indexes = List()
    for i in new_idxs:
        if i != row * board.shape[1]  + col:
            union_indexes.append(i)
    return union_indexes


@njit
def infer(piece: int, board: np.ndarray, indexes: set, 
        depth: int = 2):
    """
    depth: infer depth
    """
    ps = []
    for idx in indexes:
        row = idx // board.shape[1]
        col = idx % board.shape[0]
        board[row, col] = piece
        if check_value(board, piece, row, col) == True:
            ps.append(np.inf)
            board[row, col] = 0
            break
        elif depth > 1:
            oppnent_piece = Piece.black.value + Piece.white.value - piece
            new_indexes = indexes_union(board, indexes, row, col)
            p, r, c = infer(oppnent_piece, board, new_indexes, depth-1)
            ps.append(-p)
        else:
            ps.append(0)
        board[row, col] = 0
    ps = np.array(ps)
    i = np.random.choice(np.nonzero(ps == ps.max())[0])
    row = indexes[i] // board.shape[1]
    col = indexes[i] % board.shape[0]
    return ps[i], row, col


class Minimax(Agent):
    def __init__(self, name: str, piece: Piece, **kwargs) -> None:
        super().__init__(name, piece, **kwargs)
        if 'depth' in kwargs:
            self.depth = kwargs['depth']
        else:
            self.depth = 4
        self.indexes = List()

    def play(self, board: np.ndarray, last_row: int = 0, last_col=0, steps: int = 0):
        if steps == 0:
            self.indexes = List()
            row = board.shape[0] // 2
            col = board.shape[1] // 2
        elif steps == 1:
            self.indexes = indexes_union_init(board, last_row, last_col)
            p, row, col = infer(self.piece.value, board, self.indexes, depth=self.depth)
        else:
            self.indexes = indexes_union(board, self.indexes, last_row, last_col)
            p, row, col = infer(self.piece.value, board, self.indexes, depth=self.depth)
        board[row, col] = self.piece.value
        if len(self.indexes) == 0:
            self.indexes = indexes_union_init(board, row, col)
        else:
            self.indexes = indexes_union(board, self.indexes, row, col)
        return row, col


if __name__ == '__main__':
    board = np.zeros((9,9), dtype=np.int32)
    player0 = Minimax('black', Piece.black, depth=4)
    player1 = Minimax('white', Piece.white, depth=4)
    row = -1
    col= -1
    steps = 0
    while(True):
        row, col = player0.play(board, row, col, steps)
        show_board(board)
        steps += 1
        won, pos = check(board, player0.piece, row, col)
        if won == True:
            print("black won! ", pos)
            break
        row, col = player1.play(board, row, col, steps)
        show_board(board)
        steps += 1
        won, pos = check(board, player0.piece, row, col)
        if won == True:
            print("white won! ", pos)
            break