# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
from random import choice
from playerInterface import *

class MinimaxPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self._timeout = 10

    def getPlayerName(self):
        return "Minimax Player"

    # friend level
    def max_min(self, depth):
        if (self._board.is_game_over() or depth == 0):
            if (self._board.player_name(self) == "black"): # 'black'
                return [heuristique(self._board), None]
            else: # 'white'
                return [-heuristique(self._board), None]
        best = -float('inf')
        moves = self._board.legal_moves()
        best_moves = [] 
        for move in moves:
            mv = move
            self._board.push(move)
            res = self.min_max(self._board, depth-1)
            if (res > best):
                best_moves = []
                best_moves.append(mv)
            elif (res == best):
                best_moves.append(mv)
            best = max(best, res)
            self._board.pop()
        return [best, best_moves]

    # foe level
    def min_max(self, depth):
        if (self._board.is_game_over() or depth == 0):
            if (self._board.player_name(self) == "black"): # 'black'
                return heuristique(self._board)
            else: # 'white'
                return -heuristique(self._board)
        worst = float('inf')
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            res = self.max_min(self._board, depth-1)
            worst = min(worst, res[0])
            self._board.pop()
        return worst    

    def minimax(self, depth):
        return self.max_min(depth)

    def iterativeDeepening(self):
        start = time.time()
        end = start
        best_move = None
        depth = 1
        while(end - start < self._timeout):
            result = self.minimax(depth)
            best_move = choice(result[1])
            depth += 1
            end = time.time()
        return best_move

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        move = self.iterativeDeepening()
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



