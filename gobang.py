""" 
Gobang GUI program

Copyright (c) 2022 falwat, under MIT License.
"""
from tkinter import *
import numpy as np
from enum import Enum
from mainwindow import Mainwindow
from minimax import Minimax
from agent import Agent
from utils import Piece, check
from random_agent import RandomAgent

PIECES_IN_LINE = 5
BOARD_ROWS = 19
BOARD_COLS = 19
BOARD_GRID_SIZE = 25
BOARDER_SIZE = 3
BOARDER_PAD = 25
PIECE_RADIUS = BOARD_GRID_SIZE * 2 // 5
BOARD_WIDTH = 2 * BOARDER_PAD + BOARD_GRID_SIZE * (BOARD_COLS-1)
BOARD_HEIGHT = 2 * BOARDER_PAD + BOARD_GRID_SIZE * (BOARD_ROWS-1)


class GameState(Enum):
    Idle = 0
    Running = 1
    Over = 2

class ManualAgent(Agent):
    def __init__(self, name: str, piece: Piece) -> None:
        super().__init__(name, piece)
    
    def play(self, board: np.ndarray, steps: int):
        """dumy play, do nothing."""
        return None


class Gobang(Mainwindow):
    def __init__(self, master: Tk, player_agents: list,  **kw):
        super().__init__(master, **kw)

        self.player_agents = player_agents
        self.pieces_in_line = PIECES_IN_LINE
        self.steps = 0
        self.game_state = GameState.Idle
        self.num_wins = [0, 0]
        self.num_game = 0
        self.last_row = -1
        self.last_col = -1

        self.create_menu()
        self.canvas = Canvas(self.mainframe, width=BOARD_WIDTH, height=BOARD_HEIGHT, background='gray55')
        self.canvas.grid(row=0, column=0, sticky=NS)
        self.canvas.bind("<Button-1>", self.button_clicked)

        self.output_text = Text(self.mainframe)
        self.output_text.grid(row=1, column=0, sticky=NSEW)

        self.mainframe.rowconfigure(1, weight=1)
        self.mainframe.columnconfigure(0, weight=1)

        self.init_board()
        # set window's title.
        self.master.title('Gobang')
        # set window's geometry size
        self.master.geometry('800x650')
        self.showmessage('Ready.')

    def create_menu(self):
        self.game_menu = Menu(self.menubar)
        self.option_menu = Menu(self.menubar)
        self.repeat_menu = Menu(self.menubar)
        self.player0_menu = Menu(self.menubar)
        self.player1_menu = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.game_menu, label='Game', underline= 0)
        self.menubar.add_cascade(menu=self.option_menu, label='Option', underline=0)        
        self.option_menu.add_cascade(menu=self.player0_menu, label='Player 0', underline=7)
        self.option_menu.add_cascade(menu=self.player1_menu, label='Player 1', underline=7)
        # Add Menu Items
        self.game_menu.add_command(label='Start', command=self.start, 
                                    underline=0, accelerator='Ctrl+P')
        self.game_menu.add_command(label='Restart', command=self.restart, 
                                    underline=0, accelerator='Ctrl+R')
        self.game_menu.add_separator()
        self.game_menu.add_cascade(menu=self.repeat_menu, label='repeat', underline=5)
        self.repeat_sel = IntVar(value=0)
        self.repeat_menu.add_radiobutton(label='None', variable=self.repeat_sel, value=0)
        for i in range(1, 5):
            self.repeat_menu.add_radiobutton(label=f'{2**i * 100}', variable=self.repeat_sel, value=i)
        self.player0_sel = IntVar(value=0)
        for i, agent in enumerate(self.player_agents):
            self.player0_menu.add_radiobutton(label=agent.__name__, variable=self.player0_sel, value=i)

        self.player1_sel = IntVar(value=0)
        for i, agent in enumerate(self.player_agents):
            self.player1_menu.add_radiobutton(label=agent.__name__, variable=self.player1_sel, value=i)

    def append_output(self, msg: str):
        self.output_text.insert('end', msg + '\n')

    def init_board(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        xlim = [BOARDER_PAD, BOARDER_PAD + (BOARD_COLS-1) * BOARD_GRID_SIZE]
        ylim = [BOARDER_PAD, BOARDER_PAD + (BOARD_ROWS-1) * BOARD_GRID_SIZE]
        # boarder
        self.canvas.create_line(xlim[0]-BOARDER_SIZE, ylim[0]-BOARDER_SIZE, 
                                xlim[0]-BOARDER_SIZE, ylim[1]+BOARDER_SIZE)
        self.canvas.create_line(xlim[1]+BOARDER_SIZE, ylim[0]-BOARDER_SIZE, 
                                xlim[1]+BOARDER_SIZE, ylim[1]+BOARDER_SIZE)
        self.canvas.create_line(xlim[0]-BOARDER_SIZE, ylim[0]-BOARDER_SIZE, 
                                xlim[1]+BOARDER_SIZE, ylim[0]-BOARDER_SIZE)
        self.canvas.create_line(xlim[0]-BOARDER_SIZE, ylim[1]+BOARDER_SIZE, 
                                xlim[1]+BOARDER_SIZE, ylim[1]+BOARDER_SIZE)
        for row in range(BOARD_ROWS):
            y = BOARDER_PAD + row * BOARD_GRID_SIZE
            self.canvas.create_line(xlim[0], y, xlim[1], y)

        for col in range(BOARD_COLS):
            x = BOARDER_PAD + col * BOARD_GRID_SIZE
            self.canvas.create_line(x,ylim[0], x, ylim[1])

    def button_clicked(self, event):
        if self.game_state == GameState.Running and \
            isinstance(self.players[self.steps % 2], ManualAgent):
            player: Agent = self.players[self.steps % 2]
            col = (event.y - BOARDER_PAD + BOARD_GRID_SIZE // 2) // BOARD_GRID_SIZE
            row = (event.x - BOARDER_PAD + BOARD_GRID_SIZE // 2) // BOARD_GRID_SIZE

            if self.board[row, col] != 0:
                self.append_output('the position is not empty. try again.')
            else:
                self.put_piece(player, row, col)
                ok, pos = check(self.board, player.piece, row, col)
                if ok == True:
                    self.game_over(player, pos)
                    if self.repeat_sel != 0 and self.num_game < 2 ** self.repeat_sel.get() * 100:
                        self.after(100, self.restart)
                else:
                    self.steps += 1
                    player: Agent = self.players[self.steps % 2]
                    self.showmessage(f"{player.name}'s turn")
                    self.after(10, self.play_step)

    def put_piece(self, player: Agent, row, col):
        self.last_row = row
        self.last_col = col
        y = col * BOARD_GRID_SIZE + BOARDER_PAD
        x = row * BOARD_GRID_SIZE + BOARDER_PAD
        self.board[row, col] = player.piece.value
        if player.piece == Piece.black:
            color = 'black'
        else:
            color = 'white'
        self.canvas.create_arc(x - PIECE_RADIUS, y - PIECE_RADIUS, 
                        x + PIECE_RADIUS, y + PIECE_RADIUS, 
                        fill=color, outline=color, 
                        start=0, extent=359, width=0)

    def start(self):
        self.players = [
            self.player_agents[self.player0_sel.get()]("Black", Piece.black), 
            self.player_agents[self.player1_sel.get()]("White", Piece.white)
        ]
        self.game_state = GameState.Running
        self.showmessage(f'Start.')
        player: Agent = self.players[self.steps % 2]
        self.showmessage(f"{player.name}'s turn")
        self.after(10, self.play_step)

    def restart(self):
        self.canvas.delete('all')
        self.init_board()
        self.steps = 0
        self.last_row = -1
        self.last_col = -1
        # self.output_text.delete('0.0', 'end')
        self.start()
        self.showmessage('Restart.')

    def play_step(self):
        if self.game_state == GameState.Running and \
            not isinstance(self.players[self.steps % 2], ManualAgent):
            player: Agent = self.players[self.steps % 2]
            row, col = player.play(self.board, self.last_row, self.last_col,
                                     self.steps)
            self.put_piece(player, row, col)
            ok, pos = check(self.board, player.piece, row, col)
            if ok == True:
                self.game_over(player, pos)
                if self.repeat_sel.get() != 0 and self.num_game < 2 ** self.repeat_sel.get() * 100:
                    self.after(100, self.restart)
            elif len(np.nonzero(self.board == 0)[0]) == 0:
                self.game_state = GameState.Over
                self.num_game += 1
                self.showmessage(f"No one won. Game Over.")
                if self.repeat_sel.get() != 0 and self.num_game < 2 ** self.repeat_sel.get() * 100:
                    self.after(100, self.restart)
            else:
                self.steps += 1
                player: Agent = self.players[self.steps % 2]
                self.showmessage(f"{player.name}'s turn")
                self.after(1, self.play_step)

    def game_over(self, player: Agent, pos):
        self.game_state = GameState.Over
        self.num_game += 1
        self.num_wins[self.steps % 2] += 1
        self.append_output(f"won times: {self.num_wins[0]}, {self.num_wins[1]}")
        self.showmessage(f"{player.name} won. Game Over.")
        self.canvas.create_line(
                pos[0] * BOARD_GRID_SIZE + BOARDER_PAD, 
                pos[1] * BOARD_GRID_SIZE + BOARDER_PAD, 
                pos[2] * BOARD_GRID_SIZE + BOARDER_PAD, 
                pos[3] * BOARD_GRID_SIZE + BOARDER_PAD, 
                fill='red', width=3)



if __name__ == '__main__':
    root = Tk()
    player_agents = [ManualAgent, RandomAgent, Minimax]
    Gobang(root, player_agents)
    root.mainloop()