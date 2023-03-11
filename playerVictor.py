# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
from random import choice, random
from playerInterface import *
from fuseki.Fuseki import Fuseki
import logging, sys
from math import log, sqrt
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''
    
    _DEPTH_MONTE_CARLO = 100
    _TIMOUT_HEURISTIC_ONE_MOVE = 15
    _PROPORTION_CHUBAN = 0.1 #middle of the game
    _NB_MOVES_YUSE = 5
    _PROPORTION_YUSE = 1
    _BLACK = 1
    _WHITE = 2
    _EMPTY = 0
    _NUMBER_TURN_FUSEKI = 45

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self._opponent_move = None
        self._is_fuseki = True
        self.Fuseki = None
        self._turn = 0
        self.C = 1.4
        self.plays = {}
        self.wins = {}

    def getPlayerName(self):
        return "Monte Carlo Player 2"


    def getPlayerMove(self):
        logging.debug("MY COLOR " + str(self._mycolor))
        #logging.debug("VAL TAB DE HASHAGE 0 " + str(self._board._currentHash))

        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        logging.debug("PASS 1")
        # ne pas jouer si l'adversaire a passé et plateau gagnant
        myScore = self._board.compute_score()[self._mycolor -1]
        opponentScore = self._board.compute_score()[self._board.flip(self._mycolor) -1]
        if myScore > opponentScore and self._opponent_move == "PASS":
            return "PASS"
        logging.debug("PASS 2")
        best_move = None
        if self._turn < self._NUMBER_TURN_FUSEKI: 
            if self._turn > 0:
                best_move_string = self.Fuseki.get_move(self._opponent_move)
                best_move = self._board.str_to_move(best_move_string)
            else: 
                best_move_string = self.Fuseki.get_move(self._opponent_move)
                best_move = self._board.str_to_move(best_move_string)
        else: 
            best_move = self.get_play_MC() 
        logging.debug("Essayer de debug")
        #logging.debug("best_move" + best_move_string)
        if self._board.move_to_str(best_move) == "PASS": #Fix the pb to pass during the fuseki
            best_move = choice(self._board.legal_moves())
        logging.debug("PASS 3")
        #there is a bug of loop to fix with Fuzeki, it is a small patch before the fix
        #logging.debug(best_move)
        try:
            logging.debug("TRY")
            self._board.push(best_move) # joue le coup avec la meilleure heuristique
        except:
            #not a legal move
            logging.debug("EXCEPT")
            self._board.pop()
            while True: 
                try: 
                    logging.debug("RANDOM_MOVE")
                    best_move = choice(self._board.legal_moves())
                    logging.debug(self.whoIsWinner())
                    #logging.debug(self._board.move_to_str(best_move))
                    while self._board.move_to_str(best_move) == "PASS" and self.whoIsWinner() == -1:
                        logging.debug("WHILE")
                        best_move = choice(self._board.legal_moves())
                    self._board.push(best_move)
                except:
                    self._board.pop()
                    continue
                break
        #print("I am playing ", self._board.move_to_str(best_move))
        #print("My current board :")
        #self._board.prettyPrint()


        self._turn +=1
        return Goban.Board.flat_to_name(best_move) 


    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        self._opponent_move = move
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 
        self._turn += 1

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)
        self.Fuseki = Fuseki(color)

    def whoIsWinner(self):
        myScore = self._board.compute_score()[self._mycolor -1]
        opponentScore = self._board.compute_score()[self._board.flip(self._mycolor) -1]
        if myScore > opponentScore:
            return 1
        else:
            return -1


    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
            logging.debug("I won")
            return 
        else:
            print("I lost :(!!")
            logging.debug("I lost")






    def get_play_MC(self): 
        state = self._board._currentHash
        player = self._mycolor
        moves = [m for m in self._board.weak_legal_moves()]

        if len(moves) == 1:
            return moves[0]

        games = 0
        start = time.time()
        end = start
        while(end - start < self._TIMOUT_HEURISTIC_ONE_MOVE):    
            self.run_simulation()
            games+=1
            end = time.time()
        logging.debug("NB SIMULATIONS: " + str(games))
        moves_states = []
        for p in moves:
            try:
                self._board.push(p)
                moves_states.append((p, self._board._currentHash))
                self._board.pop()
            except:
                self._board.pop()
            

        percent_wins, move = max(
            (self.wins.get((player, S), 0) /
            self.plays.get((player, S), 1),
            p)
            for p, S in moves_states
        )
        logging.debug("% WINS MEILLEUR MOVE:" + str(percent_wins))
        return move




    def run_simulation(self):
        visited_states = set()
        state = self._board._currentHash
        player = self._mycolor

        expand = True 
        count_pop = 0

        for t in range(1, self._DEPTH_MONTE_CARLO+1):
            moves = [m for m in self._board.weak_legal_moves()]

            moves_states = []
            for p in moves:
                try:
                    self._board.push(p)
                    moves_states.append((p, self._board._currentHash))
                    self._board.pop()
                except:
                    self._board.pop()


            #si tous les noeuds fils sont deja connus, on choisit celui avec la meilleure valeur selon l'heuristique UCB
            if all(self.plays.get((player, S)) for p, S in moves_states):
                log_total = log(
                    sum(self.plays[(player, S)] for p, S in moves_states))
                value, move, state = max(
                    ((self.wins[(player, S)] / self.plays[(player, S)]) +
                    self.C * sqrt(log_total / self.plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                #sinon on choisit au hasard
                move, state = choice(moves_states)


            if expand and (player, state) not in self.plays:
                expand = False
                self._board.push(move)
                player_score = self._board.compute_score()[player-1]
                opponent_score = self._board.compute_score()[self._board.flip(player) -1]
                self._board.pop()
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = (player_score-opponent_score)/10
            
            visited_states.add((player, state))
            
            self._board.push(move)

            count_pop+= 1
            player = self._board.flip(player)

            winner = -1
            if self._board.is_game_over():
                if (self.whoIsWinner() == 1):
                    winner = self._mycolor
                else:
                    winner = self._board.flip(self._mycolor)
                break


        for k in range(count_pop):
            self._board.pop()


        for player, state in visited_states:
            if (player, state) not in self.plays:
                continue
            self.plays[(player, state)] += 1
            if player == winner: 
                self.wins[(player, state)] += 1









#########################################
#ancien monte carlo


#    def playMonteCarlo(self):
#        ''' execute the algorithm of Monte Carlo'''
#        timeout = 0.1  #temps de calcul pour l'heuristic
#
#        moves = self._board.legal_moves() # Dont use weak_legal_moves() here!
#
#        
#        if len(moves) == 0: #pas de coups possibles 
#            return "PASS"   #bug a la fin de la partie sans cette conidtion, bizarre ?
#        best_val = -1000
#        best_move = None 
#
#        moves = self._moves_selection(moves)
#        logging.debug(moves)
#
#        for move in moves: #test les heuristics sur chacun des coups possibles
#            self._board.push(move)
#            val = self.heuristic(self._TIMOUT_HEURISTIC_ONE_MOVE)
#
#            if val > best_val:
#                best_val = val
#                best_move = move
#            self._board.pop()
#        
#        return best_move
#
#    
#
#    def heuristic(self, timeout): 
#        '''Compute the heuristic of a board, global method which calls another method'''
#        return self.heuristicMonteCarlo(timeout)
#
#    def heuristicMonteCarlo(self, timeout):
#        '''Compute the heuristic of a board using a global method'''
#        start = time.time()
#        end = start
#        score = 0
#        i = 0
#        while(end - start < timeout):    
#            score += self.monteCarlo(self._mycolor, self._DEPTH_MONTE_CARLO)
#            i +=1
#            end = time.time()
#        #logging.debug("NOMBRE DITERATION DE MC: "+ str(i))
#        return score/i
#        
#
#    def monteCarlo(self, color, depth):
#        '''Travel along the tree
#            score and color : allow to add other heuristic to accurate the end value, for instance we can add a method to compute the number of stones of each colors
#            depth : deph of the montecarlo
#            more accurate example : diff_stones_board, diff_stones_captured
#        '''
#        if self._board.is_game_over() or depth == 0:
#            return self.whoIsWinner()
#        while True:
#            moves = [m for m in self._board.weak_legal_moves()]
#            move = choice(moves)
#            try:
#                self._board.push(move)
#            except:
#                self._board.pop()
#                #deux choix, soit on supprime le coup de moves mais compléxité linéaire, soit on retente en espérant ne pas retomber dessus
#                continue
#            break
#        score = self.monteCarlo(self._board.flip(color), depth-1)
#        
#        self._board.pop()
#        return score
#
#
#
#
#
#    def _moves_selection(self, moves):
#        '''Return a part from the initial population of moves'''
#        len_moves = len(moves)
#        if len_moves < self._NB_MOVES_YUSE:
#            return self._random_moves_selection(moves, int(len_moves*self._NB_MOVES_YUSE), len_moves)
#        else:
#            return self._random_moves_selection(moves, int(len_moves*self._PROPORTION_CHUBAN), len_moves)
#
#    def _random_moves_selection(self, moves, numbers, len_moves):
#        '''Return a list of numbers moves choiced randomly'''
#        moves_selected = []
#        for i in range(len(moves)):
#            len_moves_selected = len(moves_selected)
#            probability = (numbers - len_moves_selected) / (len_moves -i)
#            if (random() < probability):
#                moves_selected.append(moves[i])
#                if len_moves_selected+1 == numbers:
#                    break
#        return moves_selected
