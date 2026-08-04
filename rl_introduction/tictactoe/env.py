import numpy as np


class TicTacToe:
    
    def __init__(self, row=3, col=3):
        self.board = np.zeros((row, col), dtype=int)
        self.row = row
        self.col = col

        self.opposite = {(0,0): (row-1, col-1),
                        (row-1, col-1): (0, 0),
                        (0, col-1): (row-1, 0),
                        (row-1, 0): (0, col-1)}

        self.corners = [
            (0,0),
            (0,col-1),
            (row-1,0),
            (row-1,col-1)
        ]

    def reset(self):
        self.board.fill(0)

    def legal_moves(self):
        return [
                (i, j) 
                for i  in range(self.row) 
                for j in range(self.col)
                if self.board[i, j] == 0
                ]

    def step(self, move, player):
        x, y = move

        if self.board[x, y] != 0:
            raise ValueError("Position already occupied!")
        
        self.board[x, y] = player

    def check(self, position):
        return self.board[position]
    
    def undo(self, move):
        x, y = move
        self.board[x, y] = 0

    def winner(self):
        for i in range(self.row):
            if np.all(self.board[i, :] == 1) or np.all(self.board[:, i] == 1):
                return 1
            if np.all(self.board[i, :] == -1) or np.all(self.board[:, i] == -1):
                return -1
        if np.all(np.diag(self.board) == 1) or np.all(np.diag(np.fliplr(self.board)) == 1):
            return 1
        if np.all(np.diag(self.board) == -1) or np.all(np.diag(np.fliplr(self.board)) == -1):
            return -1
        return 0

    def is_full(self):
        return len(self.legal_moves()) == 0

    
    def get_state(self) -> tuple:
        return tuple(int(x) for x in self.board.flatten())
    


    