"""
The minimax algorithm.

Copyright (c) 2022 falwat, under MIT License.
"""
from random import choice
import numpy as np
from gobang_cli import show_board
from agent import Agent
from utils import Piece, check


def indexes_union(board: np.ndarray, indexes: set, 
                    row: int, col: int, span: int = 1):
    row_lb = max(0, row - span)
    row_ub = min(board.shape[0], row + span + 1)
    col_lb = max(0, col - span)
    col_ub = min(board.shape[1], col + span + 1)
    section = board[row_lb:row_ub, col_lb:col_ub]
    row_r, col_r = np.nonzero(section==0)
    new_idxs = (row_r + row_lb) * board.shape[1] + (col_r + col_lb)
    union_indexes = set.union(indexes, new_idxs)
    return union_indexes.difference([row * board.shape[1]  + col])
    


def infer(piece: int, board: np.ndarray, indexes: set, 
        depth: int = 2):
    """
    depth: infer depth
    """
    assert isinstance(piece, int)
    ps = []
    index_list = list(indexes)
    for idx in index_list:
        row = idx // board.shape[1]
        col = idx % board.shape[0]
        board[row, col] = piece
        if check(board, piece, row, col)[0] == True:
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
    i = choice(np.nonzero(ps == ps.max())[0])
    row = index_list[i] // board.shape[1]
    col = index_list[i] % board.shape[0]
    return ps[i], row, col


class Minimax(Agent):
    def __init__(self, name: str, piece: Piece, **kwargs) -> None:
        super().__init__(name, piece, **kwargs)
        if 'depth' in kwargs:
            self.depth = kwargs['depth']
        else:
            self.depth = 4
        self.indexes = set()

    def play(self, board: np.ndarray, last_row: int = 0, last_col=0, steps: int = 0):
        if steps == 0:
            self.indexes = set()
            row = np.random.randint(board.shape[0])
            col = np.random.randint(board.shape[1])
        else:
            self.indexes = indexes_union(board, self.indexes, last_row, last_col)
            p, row, col = infer(self.piece.value, board, self.indexes, depth=self.depth)
        board[row, col] = self.piece.value
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
        if check(board, player0.piece, row, col)[0] == True:
            break
        row, col = player1.play(board, row, col, steps)
        show_board(board)
        steps += 1
        if check(board, player0.piece, row, col)[0] == True:
            break