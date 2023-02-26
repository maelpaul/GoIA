# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
from random import choice
from playerInterface import *
import heuristic
import games

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self._timeout = 0.1 # in seconds
        self._first = 0
        self._foe_move = None
        self._turn = 0

    def getPlayerName(self):
        return "Minimax Player"

    # friend level
    def max_min(self, depth):
        if (self._board.is_game_over() or depth == 0):
            return heuristic.MonteCarloHeuristic(self._board, self._mycolor)
        best = -float('inf')
        moves = self._board.legal_moves()
        best_moves = [] 
        for move in moves:
            self._board.push(move)
            res = self.min_max(depth-1)
            best = max(best, res)
            self._board.pop()
        return best

    def test_color(self):
        if self._mycolor == self._board._BLACK:
            self._first = 1

    def first_move(self):
        first_move = self._board.name_to_flat(games.black_first_move())
        self._first = 0
        return first_move
    
    def get_next_move(self):
        next_move = games.get_next_move(self._foe_move, self._board.legal_moves(), self._turn)
        if next_move != None:
            next_move = self._board.name_to_flat(next_move)
            return next_move
        return self.iterativeDeepening()

    # foe level
    def min_max(self, depth):
        if (self._board.is_game_over() or depth == 0):
            return heuristic.MonteCarloHeuristic(self._board, self._mycolor)
        worst = float('inf')
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            res = self.max_min(depth-1)
            worst = min(worst, res)
            self._board.pop()
        return worst  

    def minimax(self, depth):
        best = -float('inf')
        best_moves = []
        moves = self._board.legal_moves()
        for move in moves:
            mv = move
            self._board.push(move)
            res = self.min_max(depth-1)
            if (res > best):
                best_moves = []
                best_moves.append(mv)
            elif (res == best):
                best_moves.append(mv)
            best = max(best, res)
            self._board.pop()
        return [best, best_moves]

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
        if self._first == 0:
            move = self.get_next_move()
        elif self._first == 1:
            move = self.first_move()
        self._turn += 1
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
        self._foe_move = move
        self._turn += 1
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self.test_color()
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")
