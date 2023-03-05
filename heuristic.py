import time
import Goban 
from random import choice
import math
import copy


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


def libertiesAndCountHeuristic(board, color):
    black_score = 0
    white_score = 0

    black_liberties = 0
    white_liberties = 0

    black_stones = 0
    white_stones = 0

    for i in range(9):
        for j in range(9):
            
            stone_color = board[board.flatten((i,j))]
            if stone_color != Goban.Board._EMPTY:
                stone_liberties = 0
                if i > 0 and board[board.flatten((i-1,j))] == Goban.Board._EMPTY:
                    stone_liberties += 1
                if j > 0 and board[board.flatten((i,j-1))] == Goban.Board._EMPTY:
                    stone_liberties += 1
                if i < 8 and board[board.flatten((i+1,j))] == Goban.Board._EMPTY:
                    stone_liberties += 1
                if j < 8 and board[board.flatten((i,j+1))] == Goban.Board._EMPTY:
                    stone_liberties += 1
                if stone_color == Goban.Board._BLACK:
                    black_liberties += stone_liberties
                    black_stones +=1

                else:
                    white_liberties += stone_liberties
                    white_stones += 1


                
    white_score += white_liberties + white_stones
    black_score += black_liberties + black_stones
            
    if color == Goban.Board._BLACK:
        return black_score - white_score
    else:
        return white_score - black_score


def secondHeuristic(board, color):
    moves = board.legal_moves()
    result = 0
    if board.is_game_over():
        return libertiesAndCountHeuristic(board, color)
    
    for move in moves:
        board.push(move)
        result += libertiesAndCountHeuristic(board,color)
        board.pop()
    
    return result + libertiesAndCountHeuristic(board, color)

def get_color(color):
    return Goban.Board._BLACK if color == Goban.Board._BLACK else Goban.Board._WHITE
