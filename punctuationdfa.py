from automata.fa.dfa import DFA

def punctuation_dfa():
    """Create DFA for punctuation."""
    trap_state = 'trap'  # Define a trap state
    input_symbols = set("(){}[];,.")  # Set of valid punctuation symbols
    states = {'q0', 'q1', trap_state}  # Include the trap state

    # Transitions for punctuation symbols
    transitions = {
        'q0': {char: 'q1' for char in "(){}[];,."},  # All valid punctuation symbols go from q0 to q1
        'q1': {}  # No transitions from q1, it is a final state
    }

    # Add trap state transitions for all symbols not explicitly handled
    for state in states:
        for symbol in input_symbols:
            if symbol not in transitions.get(state, {}):
                transitions.setdefault(state, {})[symbol] = trap_state
    transitions[trap_state] = {symbol: trap_state for symbol in input_symbols}  # Trap state handles all symbols

    return DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state='q0',
        final_states={'q1'}
    )

def test_punctuation(punctuation):
    # Get the DFA for punctuation
    dfa = punctuation_dfa()
    
    # Validate the punctuation using the DFA
    state = dfa.initial_state
    for char in punctuation:
        if char in dfa.transitions[state]:
            state = dfa.transitions[state][char]
        else:
            return False  # Invalid punctuation
    return state in dfa.final_states  # Check if it ends in a final state

# Test the function with different punctuation
if __name__ == "__main__":
    test_cases = ["(", ")", "{", "}", "[", "]", ";", ".", ",","?"]
    
    for test_case in test_cases:
        result = test_punctuation(test_case)
        print(f"Punctuation: '{test_case}', Valid: {result}")
