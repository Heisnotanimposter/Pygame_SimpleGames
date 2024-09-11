import numpy as np

class ConnectFour:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((self.rows, self.columns), dtype=int)  # 0: Empty, 1: Player 1, 2: Player 2
        self.current_player = 1

    def reset(self):
        """Reset the game board and set the current player to 1."""
        self.board = np.zeros((self.rows, self.columns), dtype=int)
        self.current_player = 1

    def is_valid_move(self, column):
        """Check if a move in the given column is valid."""
        return self.board[0, column] == 0

    def get_next_open_row(self, column):
        """Find the next available row in a column to drop a piece."""
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][column] == 0:
                return r
        return None

    def drop_piece(self, column):
        """Drop a piece into the specified column."""
        if not self.is_valid_move(column):
            return False

        row = self.get_next_open_row(column)
        self.board[row][column] = self.current_player
        self.current_player = 3 - self.current_player  # Switch players
        return True

    def check_winner(self):
        """Check for a winner (horizontal, vertical, or diagonal)."""
        # Check horizontal
        for r in range(self.rows):
            for c in range(self.columns - 3):
                if all(self.board[r][c + i] == self.current_player for i in range(4)):
                    return self.current_player

        # Check vertical
        for r in range(self.rows - 3):
            for c in range(self.columns):
                if all(self.board[r + i][c] == self.current_player for i in range(4)):
                    return self.current_player

        # Check diagonals (positive slope)
        for r in range(self.rows - 3):
            for c in range(self.columns - 3):
                if all(self.board[r + i][c + i] == self.current_player for i in range(4)):
                    return self.current_player

        # Check diagonals (negative slope)
        for r in range(self.rows - 3):
            for c in range(3, self.columns):
                if all(self.board[r + i][c - i] == self.current_player for i in range(4)):
                    return self.current_player

        # Check for a draw
        if np.count_nonzero(self.board) == self.rows * self.columns:
            return 0  # Draw

        return None  # No winner yet