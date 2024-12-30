from automata.fa.dfa import DFA

def identifier_dfa():
    # Define the trap state for invalid transitions
    trap_state = 'trap'
    
    # Define the valid input symbols (letters, digits, and underscore)
    input_symbols = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
    
    # Define the states, including the trap state
    states = {'q0', 'q1', trap_state}
    
    # Create the transitions for valid symbols
    transitions = {
        'q0': {char: 'q1' for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"},  # First character must be a letter or underscore
        'q1': {char: 'q1' for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"}  # Subsequent characters can be letters, digits, or underscores
    }

    # Add trap state transitions for all symbols not explicitly handled
    for state in states:
        for symbol in input_symbols:
            if symbol not in transitions.get(state, {}):
                transitions.setdefault(state, {})[symbol] = trap_state
    transitions[trap_state] = {symbol: trap_state for symbol in input_symbols}  # Trap state handles all symbols

    # Return the DFA object
    return DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state='q0',
        final_states={'q1'}
    )

def test_identifier(identifier):
    # Get the DFA for identifiers
    dfa = identifier_dfa()
    
    # Validate the identifier using the DFA
    state = dfa.initial_state
    for char in identifier:
        if char in dfa.transitions[state]:
            state = dfa.transitions[state][char]
        else:
            return False  # Invalid identifier
    return state in dfa.final_states  # Check if it ends in a final state

# Test the function with different identifiers
if __name__ == "__main__":
    test_cases = ["validIdentifier", "_valid123", "123invalid", "another_valid_123"]
    
    for test_case in test_cases:
        result = test_identifier(test_case)
        print(f"Identifier: '{test_case}', Valid: {result}")

