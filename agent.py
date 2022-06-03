"""
The Agent metaclass.

Copyright (c) 2022 falwat, under MIT License.
"""
import abc
import numpy as np
from utils import Piece


class Agent(metaclass=abc.ABCMeta):
    def __init__(self, name: str, piece: Piece, **kwargs) -> None:
        """
        The Agent metaclass.

        Parameters
        ----------
        name: str
            player name.
        piece: Piece 
            The pieces used by the player. Piece.black or Piece.white
        """
        self.name = name
        self.piece = piece

    @abc.abstractmethod
    def play(self, board: np.ndarray, last_row: int = 0, last_col = 0, steps: int = 0):
        """
        parameters:
        -----------
        board: np.ndarray
            M by N array. 
        last_row: int
            the row of last play. [0, M)
        last_col: int
            the col of last play. [0, N)
        steps: int
            the step number from start game. begin with 0.

        returns:
        --------
        row, col: the next position of play.
        """
        pass
