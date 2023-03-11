class State:
    def __init__(self, name):
        self._name = name
        self._next_states = []
    
    def name(self):
        return self._name

    def next_states(self):
        return self._next_states
    
    def add_next_state(self, s):
        if s not in self._next_states:
            self._next_states.append(s)

class Automaton:
    def __init__(self):
        self._initial_states = []
        self._final_states = []
        self._states = {}

    def get_state(self, s):
        return self._states[s]

    def initial_states(self):
        return self._initial_states
    
    def final_states(self):
        return self._final_states
    
    def add_initial_state(self, s):
        try:
            self._states[s]
        except:
            self._states[s] = State(s)
        if s not in self._initial_states:
            self._initial_states.append(s)

    def add_final_state(self, s):
        try:
            self._states[s]
        except:
            self._states[s] = State(s)
        if s not in self._final_states:
            self._final_states.append(s)

    def add_transition(self, s1, t, s2):
        state1 = None
        state2 = None
        transition = None
        try:
            state1 = self._states[s1]
        except:
            state1 = self._states[s1] = State(s1)
        try:
            transition = self._states[t]
        except:
            transition = self._states[t] = State(t)
        try:
            state2 = self._states[s2]
        except:
            state2 = self._states[s2] = State(s2)
        state1.add_next_state(transition)
        transition.add_next_state(state2)

