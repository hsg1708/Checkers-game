import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers import board1
from checkers.board import Board

class Game:
    def __init__(self, win):
        self.initialize_game()
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def initialize_game(self):
        # Initialize game variables
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        # check if there is a winner on the board
        return self.board.winner()

    def reset(self):
        # Reset the game to its initial state
        self.initialize_game()

    def select(self, row, col):
        if self.selected:
            # If a piece is already selected, try to move it
            result = self.move_piece(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            # If a piece is clicked, select it and show its valid moves
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def move_piece(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # If a valid move is clicked, move the piece and remove any captured pieces
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        # Draw blue circles on all valid move squares
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        # Switch the turn to the other player and reset valid moves
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        # Get the current state of the board
        return self.board

    def ai_move(self, board):
        # Move made by the AI player
        self.board = board
        self.change_turn()
