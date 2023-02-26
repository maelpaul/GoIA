import time
import Goban 
from random import choice


def randomEndGame(board, color):
    if board.is_game_over():
        (black, white) = board.compute_score()
        if color == Goban.Board._BLACK:
            return black - white
        else:
            return white - black
    
    moves = board.legal_moves() 
    move = choice(moves) 
    board.push(move)
    result = randomEndGame(board, color)
    board.pop()
    return result


def MonteCarloHeuristic(board, color):
    heuristic = 0
    for i in range(1):
        heuristic += randomEndGame(board, color)
    return heuristic