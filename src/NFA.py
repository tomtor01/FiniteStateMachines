"""
Funkcje dla poszczególnych zadań są wywoływane na końcu tego pliku.

Dane:
- plik 'nfa3.txt' zawiera automat do zadania 3. jako wejscie,
- plik 'nfa4.txt' zawiera automat do zadań 4 i 5 jako wejscie

Po wykonaniu całego programu utworzą się pliki:
- 'dfa3.txt' jako wynik zadania 3.
- 'nfa_no_eps.txt' jako wynik zadania 4.
- 'dfa5.txt' jako wynik zadania 5.
"""

class NFA:
    def __init__(self):
        self.number_of_states = 0
        self.initial_state = None
        self.final_states = set()
        self.transitions = {}  # Keys: (state, symbol); symbol==None dla epsilona

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
        # obliczanie ε-domknięcia
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
            # Dla każdego stanu, w którym się znajduje pobieram możliwe przejścia dla aktualnie przetwarzanego symbolu
            for state in current_states:
                next_states.update(self.get_target_states(state, character))
            current_states = epsilon_closure(next_states)
            if not current_states:
                return False
        return any(state in self.final_states for state in current_states)


""" Czytanie nfa z pliku """
def import_NFA_from_file(file):
    nfa = NFA()

    with open(file, 'r') as f:
        lines = f.readlines()

    transitions_data = []
    final_states = set()
    max_state = -1

    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue  # pomija puste linie
        if len(parts) == 3:
            state_from, state_to, character = int(parts[0]), int(parts[1]), parts[2]
            transitions_data.append((state_from, state_to, character))
            max_state = max(max_state, state_from, state_to)
        elif len(parts) == 1:
            state = int(parts[0])
            final_states.add(state)
            max_state = max(max_state, state)

    for _ in range(max_state + 1):
        nfa.add_state()

    nfa.mark_as_initial(0)

    for state in final_states:
        nfa.mark_as_final(state)

    for (state_from, state_to, character) in transitions_data:
        if character == "<eps>":
            nfa.add_epsilon_transition(state_from, state_to)
        else:
            nfa.add_transition(state_from, character, state_to)

    return nfa


def remove_epsilon_transitions(input_file, output_file):    # zadanie 4
    nfa = import_NFA_from_file(input_file)

    def epsilon_closure(nfa_class, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for next_state in nfa_class.get_target_states(state, None):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    new_nfa = NFA()
    for _ in range(nfa.get_number_of_states()):
        new_nfa.add_state()
    new_nfa.mark_as_initial(nfa.get_initial_state())

    # tworze alfabet bez epsilonow
    alphabet = set()
    for (state, symbol) in nfa.transitions.keys():
        if symbol is not None:
            alphabet.add(symbol)

    for s in range(nfa.get_number_of_states()):
        closure_s = epsilon_closure(nfa, {s})
        for a in alphabet:
            destination = set()
            for t in closure_s:
                destination.update(nfa.get_target_states(t, a))
            if destination:
                new_dest = set()
                for d in destination:
                    new_dest.update(epsilon_closure(nfa, {d}))
                for target in new_dest:
                    new_nfa.add_transition(s, a, target)

    for s in range(nfa.get_number_of_states()):
        closure_s = epsilon_closure(nfa, {s})
        if any(state in nfa.final_states for state in closure_s):
            new_nfa.mark_as_final(s)

    with open(output_file, 'w') as f:
        for (state, symbol), targets in new_nfa.transitions.items():
            if symbol is not None:
                for state_to in targets:
                    f.write(f"{state} {state_to} {symbol}\n")
        for state in sorted(new_nfa.final_states):
            f.write(f"{state}\n")


def convert_nfa_to_dfa(input_file, output_file):  # determinizacja nfa bez przejsc epsilonowych
    nfa = import_NFA_from_file(input_file)

    alphabet = set()
    for (state, symbol) in nfa.transitions.keys():
        if symbol is not None:
            alphabet.add(symbol)

    dfa_state_map = {}
    dfa_transitions = {}
    dfa_final_states = set()

    initial_subset = frozenset({nfa.get_initial_state()})
    dfa_state_map[initial_subset] = 0
    unprocessed = [initial_subset]
    next_state_id = 1

    while unprocessed:
        current_subset = unprocessed.pop(0)
        current_id = dfa_state_map[current_subset]
        # ustaw stan z dfa jako koncowy gdy stan z nfa w subsecie jest koncowy
        if any(state in nfa.final_states for state in current_subset):
            dfa_final_states.add(current_id)
        for symbol in alphabet:
            next_subset = set()
            for state in current_subset:
                next_subset.update(nfa.get_target_states(state, symbol))
            if not next_subset:
                continue
            next_fs = frozenset(next_subset)
            if next_fs not in dfa_state_map:
                dfa_state_map[next_fs] = next_state_id
                next_state_id += 1
                unprocessed.append(next_fs)
            dfa_transitions[(current_id, symbol)] = dfa_state_map[next_fs]

    # klasa NFA jako przechowalnia ale dla dfa z deterministycznymi przejsciami
    dfa = NFA()
    for _ in range(next_state_id):
        dfa.add_state()
    dfa.mark_as_initial(0)
    for state in dfa_final_states:
        dfa.mark_as_final(state)
    for (state, symbol), target in dfa_transitions.items():
        dfa.add_transition(state, symbol, target)

    with open(output_file, 'w') as f:
        for (state, symbol), target in dfa_transitions.items():
            f.write(f"{state} {target} {symbol}\n")
        for state in sorted(dfa.final_states):
            f.write(f"{state}\n")


def convert_nfa_with_epsilon_to_dfa(input_file):  # zadanie 5
    # używa funkcji do usuwanie epsilonowych przejść z zadania 4, po czym dokonuje determinizacji funkcją z zadania 3
    nfa_no_eps = "nfa_no_eps.txt"
    dfa = "dfa5.txt"
    remove_epsilon_transitions(input_file, nfa_no_eps)
    convert_nfa_to_dfa(nfa_no_eps, dfa)


""" Całość determinizacji nfa (zadanie 5) """
convert_nfa_with_epsilon_to_dfa("nfa4.txt")

""" Samo zadanie 3 """
convert_nfa_to_dfa("nfa3.txt", "dfa3.txt")

""" Samo zadanie 4 """
# remove_epsilon_transitions("nfa4.txt", "nfa_no_epsilon.txt")

imported_nfa = import_NFA_from_file("nfa4.txt")

# True
print(imported_nfa.accepts("00.23"))
print(imported_nfa.accepts("+5.2"))
print(imported_nfa.accepts("-3"))
print(imported_nfa.accepts("3.6534"))
print(imported_nfa.accepts("-265.6705"))
print(imported_nfa.accepts("79.123"))
print(imported_nfa.accepts("3445"))

# False
print(imported_nfa.accepts("."))
print(imported_nfa.accepts("+."))
print(imported_nfa.accepts("abc"))
