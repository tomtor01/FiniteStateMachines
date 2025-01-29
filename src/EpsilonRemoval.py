def epsilon_closure(transitions, states):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for next_state in transitions.get((state, None), []):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

def convert_NFA_to_no_epsilon(nfa_file, output_file):
    from NFA import import_NFA_from_file

    nfa = import_NFA_from_file(nfa_file)
    new_transitions = {}

    # Compute epsilon closure for each state
    epsilon_closures = {}
    for state in range(nfa.get_number_of_states()):
        epsilon_closures[state] = epsilon_closure(nfa.transitions, {state})

    # Compute new transitions
    for state in range(nfa.get_number_of_states()):
        closure = epsilon_closures[state]
        for epsilon_state in closure:
            for (from_state, symbol), target_states in nfa.transitions.items():
                if from_state == epsilon_state and symbol is not None:  # Ignore epsilon transitions
                    if (state, symbol) not in new_transitions:
                        new_transitions[(state, symbol)] = set()
                    new_transitions[(state, symbol)].update(target_states)
                    # Also, add transitions from the target state's epsilon closure
                    for target_state in target_states:
                        if target_state in epsilon_closures:
                            new_transitions[(state, symbol)].update(epsilon_closures[target_state])

    # Compute new final states
    new_final_states = set()
    for state in range(nfa.get_number_of_states()):
        closure = epsilon_closures[state]
        if any(final_state in closure for final_state in nfa.final_states):
            new_final_states.add(state)

    with open(output_file, 'w') as f:
        for (from_state, symbol), target_states in new_transitions.items():
            for target_state in target_states:
                f.write(f"{from_state} {target_state} {symbol}\n")
        for final_state in new_final_states:
            f.write(f"{final_state}\n")


convert_NFA_to_no_epsilon("nfa.txt", "nfa_no_epsilon.txt")
