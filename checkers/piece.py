from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
from checkers import board1
import pygame

class Piece:
    # Constants
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        # Piece attributes
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        # Calculate the piece's position on the board
        self.calc_pos()

    def calc_pos(self):
        # Calculate the piece's x and y coordinates on the board
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        # Promote the piece to a king
        self.king = True
    
    def draw(self, win):
        # Draw the piece on the board
        radius = SQUARE_SIZE//2 - self.PADDING
        # Draw the piece's outline
        pygame.draw.circle(win, (180, 180, 180), (self.x, self.y), radius + self.OUTLINE)
        # Draw the piece
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        # If the piece is a king, draw a crown icon on top of it
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        # Move the piece to a new position on the board
        self.row = row
        self.col = col
        # Recalculate the piece's position
        self.calc_pos()

    def __repr__(self):
        # Return the color of the piece as a string representation
        return str(self.color)
