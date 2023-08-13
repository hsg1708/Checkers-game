from copy import deepcopy
import pygame
from checkers import board1
from checkers.constants import RED, WHITE

# Minimax algorithm with alpha-beta pruning
def minimaxwitha_b(position, depth, max_player, game, alpha, beta):
    # Base cases: if depth is 0 or there is a winner, evaluate the position and return it
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            # Recursively call minimaxwitha_b with depth-1 and max_player set to False
            evaluation = minimaxwitha_b(move, depth-1, False, game, alpha, beta)[0]
            # Update maxEval and best_move if evaluation is higher than current maxEval
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
            # Update alpha value
            alpha = max(alpha, evaluation)
            # Beta pruning
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            # Recursively call minimaxwitha_b with depth-1 and max_player set to True
            evaluation = minimaxwitha_b(move, depth-1, True, game, alpha, beta)[0]
            # Update minEval and best_move if evaluation is lower than current minEval
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
            # Update beta value
            beta = min(beta, evaluation)
            # Alpha pruning
            if beta <= alpha:
                break   
        return minEval, best_move

# Simulate a move on the board and return the resulting board
def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

# Get all possible moves for a given color
def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves

# Draw the valid moves for a given piece
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
