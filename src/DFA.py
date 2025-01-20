class DFA:
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
        self.transitions[(state_from, character)] = state_to

    def get_initial_state(self):
        return self.initial_state

    def get_target_state(self, state_from, character):
        return self.transitions.get((state_from, character))

    def is_final_state(self, state):
        return state in self.final_states

    def get_number_of_states(self):
        return self.number_of_states

    def accepts(self, string):
        current_state = self.initial_state
        for character in string:
            current_state = self.get_target_state(current_state, character)
            if current_state is None:
                return False
        return self.is_final_state(current_state)


def import_DFA_from_file(file):

    dfa = DFA()
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
    # dodawanie stanow z pliku do obiektu dfa
    i = 0
    while i <= max_state:
        dfa.add_state()
        i += 1

    dfa.mark_as_initial(0)

    for final_state in final_states:
        dfa.mark_as_final(final_state)

    for state_from, state_to, character in transitions:
        dfa.add_transition(state_from, character, state_to)

    return dfa


def code_automaton():
    dfa = import_DFA_from_file("dfa_kody_pocztowe.txt")
    return dfa


dfa = code_automaton()

print(dfa.accepts("61-909")) # True
print(dfa.accepts("22-340")) # True
print(dfa.accepts("00-000")) # True
print(dfa.accepts("99-999")) # True

print(dfa.accepts("612909")) # False
print(dfa.accepts("61-90")) # False
print(dfa.accepts("000-000")) # False
print(dfa.accepts("")) # False
