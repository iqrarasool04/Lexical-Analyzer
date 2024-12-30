from automata.fa.dfa import DFA

# A list of C++ keywords
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
    all_symbols = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")  # Include other characters
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

def create_keyword_dfas():
    keyword_dfas = {}
    for keyword in cpp_keywords:
        dfa = keyword_dfa(keyword)
        keyword_dfas[keyword] = dfa
    return keyword_dfas

def identifier_dfa():
    trap_state = 'trap'
    input_symbols = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
    states = {'q0', 'q1', trap_state}
    transitions = {
        'q0': {char: 'q1' for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"},
        'q1': {char: 'q1' for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"}
    }

    for state in states:
        for symbol in input_symbols:
            if symbol not in transitions.get(state, {}):
                transitions.setdefault(state, {})[symbol] = trap_state
    transitions[trap_state] = {symbol: trap_state for symbol in input_symbols}

    return DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state='q0',
        final_states={'q1'}
    )

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

def operator_dfa():
    trap_state = 'trap'
    input_symbols = set("+-*/%=<>!&|^")
    states = {'q0', 'q1', trap_state}

    transitions = {
        'q0': {char: 'q1' for char in "+-*/%=<>!&|^"},
        'q1': {}
    }

    for state in states:
        for symbol in input_symbols:
            if symbol not in transitions.get(state, {}):
                transitions.setdefault(state, {})[symbol] = trap_state
        transitions[trap_state] = {symbol: trap_state for symbol in input_symbols}

    return DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state='q0',
        final_states={'q1'}
    )

def punctuation_dfa():
    trap_state = 'trap'
    input_symbols = set("(){}[];,.")
    states = {'q0', 'q1', trap_state}

    transitions = {
        'q0': {char: 'q1' for char in "(){}[];,."},
        'q1': {}
    }

    for state in states:
        for symbol in input_symbols:
            if symbol not in transitions.get(state, {}):
                transitions.setdefault(state, {})[symbol] = trap_state
        transitions[trap_state] = {symbol: trap_state for symbol in input_symbols}

    return DFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state='q0',
        final_states={'q1'}
    )

#def string_literal_dfa():
#    """Create DFA for string literals."""
#    states = {'q0', 'q1', 'q2', 'trap'}  # Include trap state
#    input_symbols = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_\"\\")  # Valid input symbols for a string literal (including escape characters)
#    
#    transitions = {
#        'q0': {'"': 'q1'},  # Start of string literal (q0 -> q1 on ")
#        'q1': {char: 'q1' for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"} | {'\\': 'q1', '"': 'q2'},  # Characters inside string, handling escape characters
#        'q2': {},  # Final state (end of string literal)
#        'trap': {}  # Trap state for invalid transitions
#    }
#
#    # Add trap state transitions for all invalid symbols
#    for state in states:
#        for symbol in input_symbols:
#            if symbol not in transitions.get(state, {}):
#                transitions.setdefault(state, {})[symbol] = 'trap'
#    transitions['trap'] = {symbol: 'trap' for symbol in input_symbols}  # Trap state handles all symbols
#
#    # Return the DFA object for string literals
#    return DFA(
#        states=states,
#        input_symbols=input_symbols,
#        transitions=transitions,
#        initial_state='q0',
#        final_states={'q2'}  # The final state for a valid string literal
#    )

def automata_for_string_literals():
    # Define the set of all possible input symbols for string literals (including all alphanumeric and special characters)
    input_symbols = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+[]{};:'\\|,.<>?/`~ \n\t\""
    )

    # Create the DFA for detecting string literals
    return DFA(
        states={"q0", "q1", "q2", "qf", "dead"},
        input_symbols=input_symbols,
        transitions={
            "q0": {
                **{char: "dead" for char in input_symbols},
                "\"": "q1",
            },

            "q1": {
                **{char: "q1" for char in input_symbols - {"\"", "\\"}},
                "\"": "qf",
                "\\": "q2",
            },

            # After escape character (q2) can handle specific escape sequences
            "q2": {
                **{char: "dead" for char in input_symbols},
                "n": "q1", "t": "q1", "r": "q1", "\"": "q1", "\\": "q1",
                
            },

            # Final state (qf) after closing quote
            "qf": {char: "dead" for char in input_symbols},

            # Dead state (handles invalid input)
            "dead": {char: "dead" for char in input_symbols},
        },
        initial_state="q0",
        final_states={"qf"},
    )
    
# Test cases
def test_stringliteral_automata():
    dfa = automata_for_string_literals()

    test_cases = {
        # Valid string literals
        "\"hello\"": True,
        "\"\"": True,
        "\"newline\\n\"": True,
        "\"tab\\t\"": True,
        "\"escaped quote \\\"\"": True,
        "\"escaped backslash \\\\\"": True,

        # Invalid string literals
        "hello": False,  # Missing quotes
        "\"unclosed string": False,  # Missing closing quote
        "\"invalid \\x\"": False,  # Invalid escape sequence
        "\"multiple \\\\ \\\" quotes\"": True,  # Valid string with multiple escapes
    }

    all_passed = True
    for string, expected in test_cases.items():
        try:
            result = dfa.accepts_input(string)
            if result != expected:
                print(f"Test failed for input: {string}. Expected: {expected}, Got: {result}")
                all_passed = False
        except Exception as e:
            print(f"Test raised an exception for input: {string}. Exception: {e}")
            all_passed = False

    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed.")


def build_all_dfas():
    """Build all the necessary DFAs for C++ token types."""
    return {
        'keywords': create_keyword_dfas(),
        'identifier': identifier_dfa(),
        'number': number_dfa(),
        'operator': operator_dfa(),
        'punctuation': punctuation_dfa(),
        'string_literal': automata_for_string_literals()  # Add the string literal DFA
    }

class LexicalAnalyzer:

    def __init__(self):
        self.dfas = build_all_dfas()

    def validate_with_dfa(self, token, dfa):
        """Check if the token is valid according to the DFA."""
        state = dfa.initial_state
        for char in token:
            if char in dfa.transitions[state]:
                state = dfa.transitions[state][char]
            else:
                return False
        return state in dfa.final_states

    def skip_whitespace_and_comments(self, code, i):
        """Skip whitespace and comments (both single-line and multi-line)."""
        while i < len(code):
            if code[i] in ' \t\n':  # Skip whitespace (spaces, tabs, and newlines)
                i += 1
            elif code[i:i+2] == "//":  # Single-line comment
                i = code.find("\n", i) + 1  # Skip to the next line
            elif code[i:i+2] == "/*":  # Multi-line comment
                i = code.find("*/", i) + 2  # Skip to the end of the comment
            else:
                break  # If no whitespace or comment, stop skipping
        return i

    def tokenize(self, code):
        """Tokenize the code using DFAs."""
        tokens = []
        i = 0
        while i < len(code):
            # Skip whitespace and comments
            i = self.skip_whitespace_and_comments(code, i)

            matched = False
            # First, check for string literals
            if code[i] == '"':  # Start of a string literal
                match = ""
                state = self.dfas['string_literal'].initial_state
                for j in range(i, len(code)):
                    if code[j] in self.dfas['string_literal'].input_symbols and state in self.dfas['string_literal'].transitions:
                        state = self.dfas['string_literal'].transitions[state].get(code[j], 'trap')
                        match += code[j]
                        if state in self.dfas['string_literal'].final_states:
                            tokens.append(('string_literal', match))  # Add the matched string literal token
                            i = j + 1  # Move past the string literal
                            matched = True
                            break
                    else:
                        break

            if not matched:
                # Try matching each other category (keywords, identifier, number, operator, punctuation)
                for category, dfas in self.dfas.items():
                    if category == 'keywords':
                        for keyword, dfa in dfas.items():
                            match = ""
                            state = dfa.initial_state
                            for j in range(i, len(code)):
                                if code[j] in dfa.input_symbols and state in dfa.transitions and code[j] in dfa.transitions[state]:
                                    state = dfa.transitions[state][code[j]]
                                    match += code[j]
                                    if state in dfa.final_states:
                                        tokens.append((category, match))
                                        i = j + 1
                                        matched = True
                                        break
                                else:
                                    break
                            if matched:
                                break
                    else:
                        dfa = dfas
                        match = ""
                        state = dfa.initial_state
                        for j in range(i, len(code)):
                            if code[j] in dfa.input_symbols and state in dfa.transitions and code[j] in dfa.transitions[state]:
                                state = dfa.transitions[state][code[j]]
                                match += code[j]
                                if state in dfa.final_states:
                                    if category == 'identifier':
                                        tokens.append((category, match))
                                        i = j + 1  # Move past the identifier
                                        matched = True
                                        break
                                    else:
                                        tokens.append((category, match))
                                        i = j + 1
                                        matched = True
                                        break
                            else:
                                break
                    if matched:
                        break

            # Handle error if no match found
            if not matched:
                tokens.append(("ERROR", code[i]))
                i += 1

        return tokens

    def print_tokens(self, tokens):
        """Print the tokenized output."""
        for token_type, value in tokens:
            print(f"Type: {token_type}, Value: {value}")


if __name__ == "__main__":
    code = """int main() {
    _itt = 4 + 5;
    string str = "Hello, World!";
}"""
    
    analyzer = LexicalAnalyzer()
    tokens = analyzer.tokenize(code)
    analyzer.print_tokens(tokens)



