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
                for epsilon_state in self.get_target_states(state, None):
                    if epsilon_state not in closure:
                        closure.add(epsilon_state)
                        stack.append(epsilon_state)
            return closure

        current_states = epsilon_closure({self.initial_state})
        for character in string:
            next_states = set()
            for state in current_states:
                next_states.update(self.get_target_states(state, character))
            current_states = epsilon_closure(next_states)  # Expand to epsilon closure
            if not current_states:
                return False
        return any(state in self.final_states for state in current_states)


def import_NFA_from_file(file):
    nfa = NFA()

    with open(file, 'r') as f:
        lines = f.readlines()

    transitions = []
    final_states = set()

    for line in lines:
        parts = line.strip().split()
        if len(parts) == 3:
            # Transition line: state_from, state_to, character
            state_from, state_to, character = int(parts[0]), int(parts[1]), parts[2]
            if character == "<eps>":
                nfa.add_epsilon_transition(state_from, state_to)
            else:
                nfa.add_transition(state_from, character, state_to)
        elif len(parts) == 1:
            # Final state line
            final_states.add(int(parts[0]))

    # Add states to NFA
    max_state = max(max(t[0], t[1]) for t in transitions) if transitions else 0
    for _ in range(max_state + 1):
        nfa.add_state()

    # Set initial state
    nfa.mark_as_initial(0)

    # Set final states
    for state in final_states:
        nfa.mark_as_final(state)

    return nfa


imported_nfa = import_NFA_from_file("nfa.txt")
print(imported_nfa.accepts("ba"))  # True
print(imported_nfa.accepts("b"))   # False
print(imported_nfa.accepts("a"))   # True
