import json
import Goban
from random import choice

with open("games.json") as games:
    data = json.load(games)

B_list = []
W_list = []

for dico in data:
    if dico['winner'] == 'B':
        B_list.append(dico['moves'])
    elif dico['winner'] == 'W':
        W_list.append(dico['moves'])

def black_first_move():
    first_moves = [L[0] for L in B_list]
    dico = {}
    for move in first_moves:
        if move in dico:
            dico[move] +=1
        else:
            dico[move] = 1
    max = 0
    moves = []
    for move in dico:
        if dico[move] > max:
            max = dico[move]
            moves = [move]
        elif dico[move] == max:
            moves.append(move)
    first_move = choice(moves)
    return first_move

def get_next_move(foe_move, legal_moves, turn):
    for i in range(len(legal_moves)):
        legal_moves[i] = Goban.Board.flat_to_name(legal_moves[i])
    if turn%2 == 0 and turn != 0:
        extract_moves = [[L[turn-1], L[turn]] for L in B_list if len(L) >= turn+1]
    elif turn%2 == 1: 
        extract_moves = [[L[turn-1], L[turn]] for L in W_list if len(L) >= turn+1]
    next_moves = []
    for M in extract_moves:
        if M[0] == foe_move:
            next_moves.append(M[1])
    dico = {}
    for move in next_moves:
        if move in dico:
            dico[move] +=1
        else:
            dico[move] = 1
    max = 0
    draft_moves = []
    for move in dico:
        if dico[move] > max:
            max = dico[move]
            draft_moves = [move]
        elif dico[move] == max:
            draft_moves.append(move)
    moves = []
    for move in draft_moves:
        if move in legal_moves:
            moves.append(move)
    if moves == []:
        return None
    next_move = choice(moves)
    return next_move
