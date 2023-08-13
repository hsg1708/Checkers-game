import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from checkers import board1
from minimaxwitha_b.algorithm import minimaxwitha_b

FPS = 60

# Initialize Pygame and set window caption
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers Game')
grid = [  [1,3,1],
  [1,5,1],
  [4,2,1]
]

# Get row and column values from mouse click position
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Main function
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    alpha = float('-inf')
    beta = float('inf')
    result = board1.min_path_subtraction(grid)
    while run:
        # Tick the clock
        clock.tick(FPS)

        # If it's the AI's turn, call the minimax algorithm to choose its move
        if game.turn == WHITE:
            value, new_board = minimaxwitha_b(game.get_board(), 4, WHITE, game, alpha, beta)
            game.ai_move(new_board)
            result = board1.min_path_subtraction(grid)

        # If there is a winner, print the winner and end the game loop
        if game.winner() is not None:
            print(game.winner())
            run = False
            result = board1.min_path_subtraction(grid)

        # Check for Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # If the mouse is clicked, get the row and column values and select the piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
                result = board1.min_path_subtraction(grid)

        # Update the game display
        game.update()
    
    # Quit Pygame when the game loop ends
    pygame.quit()

if __name__ == "__main__":
    main()
