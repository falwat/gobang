"""
utilities for gobang

Copyright (c) 2022 falwat, under MIT License.
"""
from enum import Enum
import numpy as np
from numba import  njit

class Piece(Enum):
    """
    Piece Enum class.
    """
    black: int = 1
    white: int = 2

def check(board: np.ndarray, piece, row: int, col: int, pieces_in_line: int = 5):
    """
    Check for winning.

    Parameters
    ----------
    board : np.ndarray
        the game board.
    piece: Piece or int
        check for Piece.black or Piece.white, or the corresponding enum value.
    row : int
        row of last piece.
    col : int
        column of last piece.
    pieces_in_line : int
        pieces in line that winning. default is 5.

    Returns
    -------
    winning : bool
        True, the player won and the game over; 
        False, the player not won and the game continue.
    pos: tuple_of_int (row0, col0, row1, col1)
        when winning is True, pos mean position of pieces in line.
    """
    if isinstance(piece, Piece):
        value = piece.value
    else:
        value = piece
    row0: int = -1
    col0: int = -1
    row1: int = -1
    col1: int = -1
    winning = False
    for t in range(4):
        if winning:
            break
        if t == 0:
            # horizon
            line = board[row]
            rows = row * np.ones(board.shape[1])
            cols = np.arange(board.shape[0])
        elif t == 1:
            # vertical
            line = board[:, col]
            rows = np.arange(board.shape[0])
            cols = col * np.ones(board.shape[1])
        elif t == 2:
            # diagnal LU->RD
            line = np.diagonal(board, col - row)
            if row < col:
                rows = np.arange(len(line))
                cols = col - row + rows
            else:
                cols = np.arange(len(line))
                rows = row - col + cols
        elif t == 3:
            fliped_row = board.shape[0] - row - 1
            # dianal LD->RU
            line = np.diagonal(np.flipud(board),  col - fliped_row)
            if row + col <= board.shape[0]:
                cols = np.arange(len(line))
                rows = row + col - cols
            else:
                rows = np.arange(board.shape[0]-1, board.shape[0]-len(line)-1, -1)
                cols = row + col - rows
                # rows = fliped_row - col + cols
        count = 0
        for i, p in enumerate(line):
            if p == value:
                if count == 0:
                    row0 = rows[i]
                    col0 = cols[i]
                count += 1
                if count == pieces_in_line:
                    row1 = rows[i]
                    col1 = cols[i]
                    winning = True
                    break
            else:
                count = 0
    return winning, (row0, col0, row1, col1)


@njit
def check_value(board: np.ndarray, value: int, row: int, col: int, pieces_in_line: int = 5):
    """
    Check for winning.

    Parameters
    ----------
    board : np.ndarray
        the game board.
    value: int
        check for enum value of Piece.black or Piece.white.
    row : int
        row of last piece.
    col : int
        column of last piece.
    pieces_in_line : int
        pieces in line that winning. default is 5.

    Returns
    -------
    winning : bool
        True, the player won and the game over; 
        False, the player not won and the game continue.
    """
    winning = False
    for t in range(4):
        if winning:
            break
        if t == 0:
            # horizon
            line = board[row]
            rows = row * np.ones(board.shape[1])
            cols = np.arange(board.shape[0])
        elif t == 1:
            # vertical
            line = board[:, col]
            rows = np.arange(board.shape[0])
            cols = col * np.ones(board.shape[1])
        elif t == 2:
            # diagnal LU->RD
            offset = col - row
            line = np.diag(board, offset)
            if row < col:
                rows = np.arange(len(line))
                cols = col - row + rows
            else:
                cols = np.arange(len(line))
                rows = row - col + cols
        elif t == 3:
            fliped_row = board.shape[0] - row - 1
            # dianal LD->RU
            line = np.diag(np.flipud(board),  col - fliped_row)
            if row + col <= board.shape[0]:
                cols = np.arange(len(line))
                rows = row + col - cols
            else:
                rows = np.arange(board.shape[0]-1, board.shape[0]-len(line)-1, -1)
                cols = row + col - rows
                # rows = fliped_row - col + cols
        count = 0
        for i, p in enumerate(line):
            if p == value:
                count += 1
                if count == pieces_in_line:
                    winning = True
                    break
            else:
                count = 0
    return winning


def show_board(board: np.ndarray):
    """
    Show board.

    Use 'x' for black pieces, 'o' for white pieces, and '.' for blank place.

    Parameters
    ----------
    board: np.ndarray
        the game board.
    """
    print('========' + '==='*board.shape[1])
    line = '   |'
    for col in range(board.shape[1]):
        line += f'{col:2d} '
    print(line + '|')
    print('---+' + '---'*board.shape[1] + '+---')
    for row in range(board.shape[0]):
        line = f'{row:2d} |'
        for col in range(board.shape[1]):
            if board[row, col] == Piece.black.value:
                line += ' x '
            elif board[row, col] == Piece.white.value:
                line += ' o '
            else:
                line += ' . '
        print(line + f'|{row:2d}')
    print('---+' + '---'*board.shape[1] + '+---')
    line = '   |'
    for col in range(board.shape[1]):
        line += f'{col:2d} '
    print(line + '|')
    print('========' + '==='*board.shape[1])