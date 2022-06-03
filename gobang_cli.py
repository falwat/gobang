"""
Gobang CLI(Command Line Interface) program.

Copyright (c) 2022 falwat, under MIT License.
"""
import numpy as np
from agent import Agent
from utils import Piece, check, show_board

class ManualAgent(Agent):
    def __init__(self, name: str, piece: Piece) -> None:
        super().__init__(name, piece)

    def play(self, board: np.ndarray, last_row: int = 0, last_col=0, steps: int = 0):
        while True:
            pos = input(f"Input {self.name} position(row,col):")
            row, col = [int(s) for s in pos.split(',')]
            if board[row][col] == 0:
                board[row][col] = self.piece.value
                break
            else:
                print("Error: The position is not empty! Try again.")
        return row, col

class Game:
    def __init__(self, board: np.ndarray, pieces_in_line: int=5) -> None:
        self.pieces_in_line = pieces_in_line
        self.board = board
        self.steps = 0

    def start(self, players: list):
        self.board[:,:] = 0
        self.steps = 0
        show_board(self.board)
        while True:
            player: Agent = players[self.steps % 2]
            row, col = player.play(self.board, self.steps)
            show_board(self.board)
            self.steps += 1
            if check(self.board, player.piece, row, col)[0]:
                print(f"{player.name} win!")
                break



if __name__ == "__main__":
    board = np.zeros((9,9))
    game = Game(board)
    black_player = ManualAgent('black', Piece.black)
    white_player = ManualAgent('white', Piece.white)
    game.start([black_player, white_player])
