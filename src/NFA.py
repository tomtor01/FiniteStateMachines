class NFA:
    def __init__(self):
        self.number_of_states = 0
        self.initial_state = None
        self.final_states = set()
        self.transitions = {}

    def add_state(self):
        state = self.number_of_states
        self.number_of_states += 1
        return state

    def mark_as_initial(self, state):
        self.initial_state = state

    def mark_as_final(self, state):
        self.final_states.add(state)

    def add_transition(self, state_from, character, state_to):
        if (state_from, character) not in self.transitions:
            self.transitions[(state_from, character)] = set()
        self.transitions[(state_from, character)].add(state_to)

    def add_epsilon_transition(self, state_from, state_to):
        if (state_from, None) not in self.transitions:
            self.transitions[(state_from, None)] = set()
        self.transitions[(state_from, None)].add(state_to)

    def get_initial_state(self):
        return self.initial_state

    def get_target_states(self, state_from, character):
        return self.transitions.get((state_from, character), set())

    def is_final_state(self, state):
        return state in self.final_states

    def get_number_of_states(self):
        return self.number_of_states

    def accepts(self, string):
        def epsilon_closure(states):
            closure = set(states)
            stack = list(states)
            while stack:
                state = stack.pop()
                for epsilon_state in self.get_target_states(state, None):  # Process epsilon transitions
                    if epsilon_state not in closure:
                        closure.add(epsilon_state)
                        stack.append(epsilon_state)
            return closure

        # Start with the epsilon closure of the initial state
        current_states = epsilon_closure({self.initial_state})
        for character in string:
            next_states = set()
            for state in current_states:
                next_states.update(self.get_target_states(state, character))
            current_states = epsilon_closure(next_states)  # Expand to epsilon closure
            if not current_states:
                return False
        return any(state in self.final_states for state in current_states)


nfa_eps = NFA()

state_0 = nfa_eps.add_state()
state_1 = nfa_eps.add_state()
state_2 = nfa_eps.add_state()
state_3 = nfa_eps.add_state()

nfa_eps.add_transition(state_0, 'a', state_1)
nfa_eps.add_epsilon_transition(state_1, state_2)
nfa_eps.add_transition(state_2, 'b', state_3)

nfa_eps.mark_as_initial(state_0)
nfa_eps.mark_as_final(state_3)

print(nfa_eps.accepts("ab"))  # True
print(nfa_eps.accepts("a"))  # False
print(nfa_eps.accepts(""))  # False


def import_NFA_from_file(file):     # zadanie 2

    nfa = NFA()
    with open(file, 'r') as f:
        lines = f.readlines()

    transitions = []
    final_states = set()

    for line in lines:
        parts = line.strip().split()
        # jesli linia sklada sie z 3 elementow to tworze przejscie
        if len(parts) == 3:
            state_from, state_to, character = int(parts[0]), int(parts[1]), parts[2]
            transitions.append((state_from, state_to, character))
        # jesli z jednego to dodaje stany koncowe
        elif len(parts) == 1:
            final_states.add(int(parts[0]))

    # wyznaczenie ilosci stanow
    max_state = max(max(states[0], states[1]) for states in transitions) if transitions else 0
    # dodawanie stanow z pliku do obiektu nfa
    i = 0
    while i <= max_state:
        nfa.add_state()
        i += 1

    nfa.mark_as_initial(0)

    for final_state in final_states:
        nfa.mark_as_final(final_state)

    for state_from, state_to, character in transitions:
        nfa.add_transition(state_from, character, state_to)

    return nfa


import_NFA_from_file()