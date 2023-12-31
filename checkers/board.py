import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from checkers import board1

from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    # Draw checkerboard pattern on the screen
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Evaluate the current state of the board
    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 2 - self.red_kings * 2)

    # Get all the pieces of a particular color
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    # Move a piece to a new position on the board
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        # If the piece reaches the end of the board, promote it to a king
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    # Get the piece at a given position
    def get_piece(self, row, col):
        return self.board[row][col]

    # Initialize the board
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    # Draw the pieces on the board
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    # Remove a piece from the board
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    # Check if there is a winner
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None

    # Get all the valid moves for a given piece
    def get_valid_moves(self, piece):
        # Initialize an empty dictionary to store the valid moves for the given piece
        moves = {}
        # Get the left and right positions of the piece
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # If the piece is red or a king, update moves by traversing left and right
        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        # If the piece is white or a king, update moves by traversing left and right
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        # Initialize an empty dictionary to store the valid moves while traversing left
        moves = {}
        # Initialize an empty list to keep track of the pieces that were skipped
        last = []
        # Loop through the rows while traversing left
        for r in range(start, stop, step):
            if left < 0:
                # If the left position is less than 0, break the loop
                break
            
            # Get the current piece at the given row and left position
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    # If there are skipped pieces but the last list is empty, break the loop
                    break
                elif skipped:
                    # If there are skipped pieces, update the moves dictionary
                    moves[(r, left)] = last + skipped
                else:
                    # If there are no skipped pieces, update the moves dictionary
                    moves[(r, left)] = last
                
                if last:
                    # If there are skipped pieces, recursively update the moves dictionary
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                # If the current piece is the same color as the given piece, break the loop
                break
            else:
                # If the current piece is a different color, add it to the last list
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        # Initialize an empty dictionary to store the valid moves while traversing right
        moves = {}
        # Initialize an empty list to keep track of the pieces that were skipped
        last = []
        # Loop through the rows while
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
