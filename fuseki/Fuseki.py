from .Automaton import Automaton, State
from .white_games import white_games
from .black_games import black_games
from random import choice
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class Fuseki:
    '''Class which gives the move to play at the beginning of the game'''
    _BLACK = 1
    _WHITE = 2
    _EMPTY = 0

    def __init__(self, color):
        '''Initialise the automaton, start to create the states then add the transtion
        With this rule https://senseis.xmp.net/?TrompTaylorRules, the black color starts. 
        Thus, if the color is white, you need to init with a last_opponent_move different from None
        '''
        self._turn = 0
        self._color = color
        self._automaton = Automaton()
        self._current_state = None

        games = white_games if color == self._WHITE else black_games
        for game in games:
            plays = game["moves"]
            count_plays = len(plays)
            self._automaton.add_initial_state(plays[0])
            for k in range(1, count_plays-1):
                self._automaton.add_transition(plays[k-1], plays[k], plays[k+1])
            self._automaton.add_final_state(plays[count_plays-1])

        if color == self._BLACK:
            self._current_state = choice(self._automaton.initial_states())

    def get_move(self, last_opponent_move):
        '''Return the move to play
           Strategy : check if the opponent move is a transition from our previous move 
                      if it is we take a random move from the next
                      else we choose a random move then 
            Improve : not choose a random move but a move in the same area Fixed
            Bug : can return a move already choose 
                  no consider a final state
        ''' 
        logging.debug("get_move")
        if self._turn > 0:
            logging.debug("Turn > 0")
            state = self._automaton.get_state(self._current_state)
            next_states = state.next_states()
            try: 
                # bug to fixed can loop
                self._current_state = choice(next_states[last_opponent_move].next_states()).name()
                # logging.debug(self._current_state)
                return self._current_state
            except:
                # logging.debug(choice(next_states).name())
                # logging.debug([s.name() for s in choice(next_states).next_states()])
                # logging.debug(choice(choice(next_states).next_states()).name())
                close_state = self._closeState(last_opponent_move, next_states)
                self._current_state = choice(close_state.next_states()).name()
                return self._current_state
        else:
            self._turn += 1
            if last_opponent_move:
                try:
                    state = self._automaton.get_state(last_opponent_move)
                    self._current_state = choice(state.next_states()).name()
                except: 
                    state = choice(self._automaton.initial_states)
                    self._current_state = self._closeState(last_opponent_move, next_states).name()
            #else black and return current_state compote during the init
            return self._current_state

    def _closeState(self, state, next_states):
        '''Return the next state the more closed to the initial state to play
           Complexity : O(n) with n (length of next_state), worse complexity than choice
        '''
        minimum = self._score(state, next_states[0].name())
        best_state = next_states[0]
        for next_state in next_states[1:]:
            current_value = self._score(state, next_state.name())
            if current_value < minimum: 
                minimum = current_value
                best_state = next_state
        return best_state

    def _score(self, state, next_state):
        '''Compute a score with the next state to find a play close to the initial state to play
           Return the score, the lowest score is the best
           Complexity : O(1) 
        '''
        if state == "PASS" or next_state == "PASS":
            return 100
        return abs(ord(state[0])-ord(next_state[0])) + abs(int(state[1])-int(next_state[1]))
if __name__ == '__main__':
    fuzeki = Fuseki(1)
    print(fuzeki.get_move("A1"))
    print(fuzeki._score("D1", "D4"))
    print(fuzeki._score("D1", "D8"))
    print(fuzeki._score("D1", "D1"))
    print(fuzeki._score("D1", "J4"))
    print(fuzeki._score("D1", "J8"))
