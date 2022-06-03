"""
Random Agent.

The RandomAgent Just randomly place a piece in a blank position.

Copyright (c) 2022 falwat, under MIT License.
"""
from secrets import choice
import numpy as np
from utils import Piece
from agent import Agent


class RandomAgent(Agent):
    def __init__(self, name: str, piece: Piece, **kwargs) -> None:
        super().__init__(name, piece, **kwargs)

    def play(self, board: np.ndarray, last_row: int = 0, last_col=0, steps: int = 0):
        """
        Just randomly place a piece in a blank position.
        """
        pos = np.nonzero(board == 0)
        i = choice(range(pos[0]))
        row = pos[0][i]
        col = pos[1][i]
        return row, col
