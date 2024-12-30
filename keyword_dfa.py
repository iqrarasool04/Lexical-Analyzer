# A list of C++ keywords
import re
from automata.fa.dfa import DFA
cpp_keywords = [
      'int', 'float', 'double', 'char', 'bool', 'string', 'if', 'else',
            'while', 'for', 'do', 'switch', 'case', 'default', 'break',
            'continue', 'return', 'class', 'public', 'private', 'protected',
            'namespace', 'using', 'new', 'delete', 'main'
]
def keyword_dfa(keyword):
    """Create a DFA for a specific keyword."""
    states = {f"q{i}" for i in range(len(keyword) + 1)} | {"trap"}
    input_symbols = set(keyword)  # Set of valid input symbols
    transitions = {state: {} for state in states}

    # Define valid transitions for the keyword
    for i in range(len(keyword)):
        transitions[f"q{i}"][keyword[i]] = f"q{i+1}"

    # Add trap state transitions for all symbols
    all_symbols = set(keyword)  # Expand this as needed for more general input sets
    for state in states:
        for symbol in all_symbols:
            if symbol not in transitions[state]:
                transitions[state][symbol] = "trap"
        transitions["trap"][symbol] = "trap"

    # Add the final state with no outgoing transitions
    transitions[f"q{len(keyword)}"] = {symbol: "trap" for symbol in all_symbols}

    return DFA(
        states=states,
        input_symbols=all_symbols,
        transitions=transitions,
        initial_state="q0",
        final_states={f"q{len(keyword)}"},
    )
# Create a DFA for each C++ keyword
def create_keyword_dfas():
    keyword_dfas = {}
    for keyword in cpp_keywords:
        dfa = keyword_dfa(keyword)  # Use the keyword_dfa function to create a DFA for each keyword
        keyword_dfas[keyword] = dfa
    return keyword_dfas

# Use the DFAs to validate an input string
def validate_keywords_in_code(code):
    keyword_dfas = create_keyword_dfas()
    tokens = []
    
    i = 0
    while i < len(code):
        matched = False
        
        # Try to match the current substring with each keyword DFA
        for keyword, dfa in keyword_dfas.items():
            match = ""
            state = dfa.initial_state
            
            # Check if the substring starting at position i matches the keyword DFA
            for j in range(i, len(code)):
                if code[j] in dfa.input_symbols and state in dfa.transitions and code[j] in dfa.transitions[state]:
                    state = dfa.transitions[state][code[j]]
                    match += code[j]
                    if state in dfa.final_states:
                        tokens.append((keyword, match))  # Match found, store token
                        i = j + 1
                        matched = True
                        break
                else:
                    break
            if matched:
                break
        if not matched:
            i += 1  # Move to next character if no match is found
    
    return tokens

# Test the function
# code = "int main() { return 0; }"
tokens = validate_keywords_in_code("protected")
print(tokens)
