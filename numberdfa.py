from automata.fa.dfa import DFA

def number_dfa():
    """Create DFA for numbers."""
    return DFA(
        states={'q0', 'q1'},
        input_symbols=set("0123456789"),
        transitions={
            'q0': {char: 'q1' for char in "0123456789"},
            'q1': {char: 'q1' for char in "0123456789"}
        },
        initial_state='q0',
        final_states={'q1'}
    )

def test_number(number):
    # Get the DFA for numbers
    dfa = number_dfa()
    
    # Validate the number using the DFA
    state = dfa.initial_state
    for char in number:
        if char in dfa.transitions[state]:
            state = dfa.transitions[state][char]
        else:
            return False  # Invalid number
    return state in dfa.final_states  # Check if it ends in a final state

# Test the function with different numbers
if __name__ == "__main__":
    test_cases = ["12345", "00123", "12a45", "456"]
    
    for test_case in test_cases:
        result = test_number(test_case)
        print(f"Number: '{test_case}', Valid: {result}")
