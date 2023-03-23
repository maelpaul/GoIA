import Goban
import time
import random
from playerInterface import *
import math
import copy
import numpy as np


class Node:
    def __init__(self, board,parent=None, move=None, color=None):
        self.parent = parent
        self.board = board
        self.move = move
        self.color = color
        self.visits = 0
        self.wins = 0
        self.depth = 0
        self.children = []

    def print_node(self):
        print("board",self.board)
        print("move",self.move)
        print("visits",self.visits)
        print("wins",self.wins)
        print("parent",self.parent.move)

    def add_child(self, move, color):
        board_copy = copy.deepcopy(self.board)
        child = Node(parent=self, move=move,color=color,board=board_copy)
        self.children.append(child)
        if (board_copy.flat_to_name(move) in child.board.legal_moves()):
            child.board.push(move)
        child.depth = self.depth + 1
        return child

    def fully_expanded(self):
        return len(self.children) == len(self.legal_moves())

    def update_parents(self):
        if self.parent is not None:
            self.visits += 1
            self.parent.update_parents()
        if self.parent is None:
            self.visits += 1

    def update(self,result):
        if result is None:
            return
        self.wins += result
        self.visits += 1
        if self.parent is not None:
            self.parent.update(result)
        if self.parent is None: 
            exit
    
    def best_child(self, c=1.4):
        choices_weights = [(child.wins / (child.visits+1) if child.visits > 0 else 0) + c * math.sqrt((2 * math.log(self.visits) / (child.visits+1) if child.visits > 0 else 0)) for child in self.children]
        if (len(choices_weights)==0):
            node = Node(board=self.board)
            node.move = -1
            return node
        return self.children[choices_weights.index(max(choices_weights))] if len(choices_weights)>0 else Node(board=self.board)

    def legal_moves(self):
        return self.board.legal_moves()

    def simulate(self):
        board = copy.deepcopy(self.board)
        current_color = self.color
        result = 0
        while not board.is_game_over():
            moves = board.legal_moves()
            move = random.choice(moves)
            board.push(move)
            current_color = Goban.Board.flip(current_color)
        result = board.result()
        if (result == '1-0' and self.color == "black") :
            return 1
        if (result == '0-1' and self.color == "black"):
            return -1
        return 0

class myPlayer(PlayerInterface):
    openings_black = ["E5", "E3", "F4", 'G4', 'E7', 'C6', 'E4', 'G6', 'G5', 'D3']
    openings_white = ["E5", "E7", "F4", 'G4', 'E4', 'E3', 'G5', 'G6', 'C6', 'D3']

    def __init__(self, time=20):
        self.time = time
        self._mycolor = None
        self.tree = None
        self.name = "montecarlo"
        self.last_play = -1
        self._board = Goban.Board()

    def getPlayerName(self):
        return self.name

    def get_play_time(self):
        return self.time

    def other_color(self):
        if (self._mycolor == "white"):
            return "black"
        else:
            return "white"

        self._board.push(move)
    def expand(self):
        node = self.tree
        while not node.fully_expanded() and node.visits > 0 and node.children != []:
            node = node.best_child()
        if not node.fully_expanded():
            move = random.choice(node.legal_moves())
            node = node.add_child(move, self._mycolor)
        result = 0  
        if not node.board.is_game_over() and node.parent is not None:  
            result = node.simulate()
        node.update(result)

    def get_group_liberties( self, group):
    #Fonction qui compte le nombre de libertés d'un groupe de pierres donné sur le plateau de jeu.
        board=self._board
        liberties = set()
        for stone in group:
            for j in board._get_neighbors(stone):
                if board.__getitem__(j) == 0:
                    liberties.add((j))
        return len(liberties)


    def get_groups(self, color):
        #Fonction qui retourne une liste de tous les groupes de pierres présents sur le plateau de jeu.
        board=self._board
        groups = []
        visited = set()
        for i in range(board.__len__()):
                if board.__getitem__(i) == color and i not in visited:
                    # Si une pierre n'a pas encore été visitée, on crée un nouveau groupe de pierres et on le visite.
                    group = set()
                    self.visit_group( i, group, visited)
                    groups.append(group)
        return groups



    def visit_group(self, stone, group, visited):
        
        #Fonction récursive qui visite toutes les pierres d'un groupe de pierres donné sur le plateau de jeu.
        board=self._board
        group.add(stone)
        visited.add(stone)
        for j in (board._get_neighbors(stone)):
            if j not in visited and board.__getitem__(j) == board.__getitem__(stone):
                # Si la pierre voisine n'a pas encore été visitée et appartient au même joueur, on la visite également.
                self.visit_group( j, group, visited)

 
        
    def heuristique2(self):
        score=0 
        for group in self.get_groups(self._mycolor):
            liberties = self.get_group_liberties( group)
            if liberties == 1:
                # Si un groupe n'a qu'une seule liberté, il est vulnérable et donc moins favorable.
                score -= len(group)
            else:
                # Sinon, le score est augmenté en fonction du nombre de libertés du groupe.
                score += len(group) + liberties

        controlled_territory = self._board.compute_score()
        score+= controlled_territory[(self._mycolor-1)%2]
        score-=controlled_territory[self._mycolor%2]
        return score

    def MaxValue(self, alpha, beta, depth):
        if(depth==0 or self._board.is_game_over() == True):
                heuristique=self.heuristique2()
                return heuristique
        else:
            positions=self._board.legal_moves()
            minvalue=0
            for position in positions:
                self._board.push(position)
                minvalue=self.MinValue(alpha, beta, depth-1)
                if(minvalue>alpha):                        
                    alpha=minvalue
                self._board.pop()
                if(alpha>=beta):
                    return beta
                return alpha
    def MinValue(self, alpha, beta, depth):
        if(depth==0 or self._board.is_game_over() == True):      
            return self.heuristique2()
        else:
            position=self._board.legal_moves()
            for i in position:
                self._board.push(i)
                beta=min(beta, self.MaxValue( alpha, beta, depth-1 ))
                self._board.pop()
                if(alpha>=beta):
                    return alpha
            return beta 


    def alphabeta(self, depth):
        alpha=-math.inf
        beta=math.inf
        best_score=-math.inf 
        best_action=None
        for action in self._board.legal_moves():
            self._board.push(action)
            score=self.MinValue(alpha, beta, depth-1)
            if(score>best_score):
                best_score=score
                best_action=action
            self._board.pop()
        return best_action
    
    def getPlayerMove(self):
        test = False
        depth = 4
        openings = self.openings_black if self._mycolor == 1 else self.openings_white
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        if (len(self._board.legal_moves()) >= 72):
            move = "PASS"
            for i in openings:
                if self._board.name_to_flat(i) in self._board.legal_moves():
                    move = self._board.name_to_flat(i)
                    test = True
                    break
            if (move != "PASS"):
                self._board.push(move)
                return self._board.flat_to_name(move)
        elif(len(self._board.legal_moves()) <= 20):
            move=self.alphabeta(depth)    
            self._board.push(move)
            return self._board.flat_to_name(move)
        else:
            if self.tree is None:
                self.tree = Node(parent=None, move=None, color=self._mycolor,board = self._board)
                self.tree.board = copy.copy(self._board)
            else:
                for child in self.tree.children:
                    if (self._board.flat_to_name(child.move) == self._board._historyMoveNames[-2] and len(self._board._historyMoveNames[-2])>=3):
                        self.tree = self.tree.add_child(self._board.name_to_flat(self._board._historyMoveNames[-2]),self._mycolor)
                        self.tree = self.tree.add_child(self._board.name_to_flat(self._board._historyMoveNames[-1]),self.other_color())
                        self.tree.parent = None
                        break
                else:
                    board = copy.copy(self._board)
                    self.tree = Node(parent=None, move=None, color=self._mycolor, board = board)
            start_time = time.time()
            while time.time() - start_time < self.time:
                self.expand()
            node = self.tree.best_child()
            self._board.push(node.move)
            return node.board.flat_to_name(node.move)

    def playOpponentMove(self, move):
        print("Opponent played ", move, "i.e. ", move) # New here
        self._board.push(Goban.Board.name_to_flat(move)) 
        
    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")