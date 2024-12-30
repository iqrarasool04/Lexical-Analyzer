from automata.fa.dfa import DFA
import re

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
        self.errors = []
        self.tokens = []

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

    def log_error(self, line, column, message):
        """Log an error with line and column details."""
        self.errors.append(f"Error at line {line}, column {column}: {message}")

    def checking_unterminated_string(self, input_text, start_index):
        """DFA-based function to validate a string literal."""
        state = "q0"
        index = start_index
        line, column = self.get_line_column(start_index, input_text)

        valid_escape_chars = {"n", "t", "r", "\"", "\\"}
        while index < len(input_text):
            char = input_text[index]

            if state == "q0":
                if char == "\"":
                    state = "q1"
                else:
                    return None, start_index  # Not a string literal, return control to main tokenizer.

            elif state == "q1":
                if char == "\"":
                    state = "qf"
                    index += 1
                    break
                elif char == "\\":
                    state = "q2"
                elif char == "\n":
                    self.log_error(line, column, "Unterminated string literal.")
                    return None, index
                # Stay in q1 for any valid string character.
            
            elif state == "q2":
                if char in valid_escape_chars:
                    state = "q1"
                else:
                    self.log_error(line, column, f"Invalid escape sequence: \\{char}")
                    return None, index
            
            index += 1

        if state != "qf":
            self.log_error(line, column, "Unterminated string literal.")
            return None, index

        return input_text[start_index:index], index

    def get_line_column(self, index, text):
        """Helper function to calculate line and column number from index."""
        lines = text[:index].split("\n")
        line_number = len(lines)
        column_number = len(lines[-1]) + 1
        return line_number, column_number
    
    def check_token_validity_automata(self):
        # Build the DFA
        states = {"q0"}  # Include the initial state explicitly
        alphabet = set()  # All valid characters (a-z, etc.)
        transitions = {}  # Transition function
        start_state = "q0"  # Initial state
        accept_states = set()  # Final states

        # Helper function to add transitions for a keyword
        def add_keyword_to_dfa(keyword):
            current_state = start_state
            for char in keyword:
                next_state = f"{current_state}_{char}"
                alphabet.add(char)
                states.add(next_state)
                transitions[(current_state, char)] = next_state
                current_state = next_state
            # Mark the last state as an accept state
            accept_states.add(current_state)

        # Add all keywords to the DFA
        for keyword in cpp_keywords:
            add_keyword_to_dfa(keyword)

        # Add reject state for invalid transitions
        reject_state = "q_reject"
        states.add(reject_state)
        for state in states:
            for char in alphabet:
                if (state, char) not in transitions:
                    transitions[(state, char)] = reject_state

        # Define the DFA
        return DFA(
            states=states,
            input_symbols=alphabet,
            transitions={
                state: {char: transitions.get((state, char), reject_state) for char in alphabet}
                for state in states
            },
            initial_state=start_state,
            final_states=accept_states
        )

    # Function to test a token
    def is_cpp_keyword(self, dfa, token):
        return dfa.accepts_input(token)

    # def validate_number_format(self, number, line, column):
    #     dfa = DFA(
    #         states={'q0', 'q1', 'q2', 'q3'},
    #         input_symbols={'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-'},
    #         transitions={
    #             'q0': {'-': 'q1', **{str(i): 'q1' for i in range(10)}},
    #             'q1': {**{str(i): 'q1' for i in range(10)}, '.': 'q2'},
    #             'q2': {**{str(i): 'q3' for i in range(10)}},
    #             'q3': {**{str(i): 'q3' for i in range(10)}},
    #         },
    #         initial_state='q0',
    #         final_states={'q1', 'q3'}
    #     )

    #     if not dfa.accepts_input(number):
    #         self.log_error(line, column, "Invalid number format.")


    # def validate_escape_sequences(self, string, line, column):

    #     dfa = DFA(
    #         states={"q0", "q1", "q_accept"},
    #         input_symbols={"\\", "n", "t"},
    #         transitions={
    #             "q0": {"\\": "q1"},
    #             "q1": {"n": "q_accept", "t": "q_accept"},
    #         },
    #         initial_state="q0",
    #         final_states={"q_accept"}
    #     )

    #     if not dfa.accepts_input(string):
    #         self.log_error(line, column, f"Invalid escape sequence: {string}")

    
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



import unittest

class TestLexicalAnalyzer(unittest.TestCase):
    def test_validate_number_format(self):
        lexical_analyzer = LexicalAnalyzer()

        # Valid Numbers
        lexical_analyzer.validate_number_format("123", 1, 1)  # No error
        lexical_analyzer.validate_number_format("123.45", 1, 1)  # No error
        lexical_analyzer.validate_number_format("-123", 1, 1)  # No error
        lexical_analyzer.validate_number_format("0.123", 1, 1)  # No error
        lexical_analyzer.validate_number_format("123.", 1, 1)  # No error

        # Invalid Numbers
        lexical_analyzer.validate_number_format("123..45", 1, 1)  # Error
        lexical_analyzer.validate_number_format("123.45.67", 1, 1)  # Error
        lexical_analyzer.validate_number_format("abc", 1, 1)  # Error
        lexical_analyzer.validate_number_format(".123", 1, 1)  # Error

        assert len(lexical_analyzer.errors) == 4  # Should catch 4 errors

    def test_validate_escape_sequences(self):
        lexical_analyzer = LexicalAnalyzer()

        # Valid escape sequences
        lexical_analyzer.validate_escape_sequences("\\n", 1, 1)  # No error
        lexical_analyzer.validate_escape_sequences("\\t", 1, 1)  # No error
        lexical_analyzer.validate_escape_sequences("\\r", 1, 1)  # No error
        lexical_analyzer.validate_escape_sequences("\\\\", 1, 1)  # No error
        lexical_analyzer.validate_escape_sequences('\\"', 1, 1)  # No error

        # Invalid escape sequences
        lexical_analyzer.validate_escape_sequences("\\a", 1, 1)  # Error
        lexical_analyzer.validate_escape_sequences("\\x", 1, 1)  # Error
        lexical_analyzer.validate_escape_sequences("\\z", 1, 1)  # Error
        lexical_analyzer.validate_escape_sequences("\\p", 1, 1)  # Error

        assert len(lexical_analyzer.errors) == 4  # Should catch 4 errors

if __name__ == "__main__":
    unittest.main()



# analyzer = LexicalAnalyzer()

# test_cases = [
#     ("\"Hello World\"", 0),  # Valid string literal
#     ("\"Hello\nWorld", 0),  # Unterminated string literal due to newline
#     ("\"Hello \\x World\"", 0),  # Invalid escape sequence
#     ("Not a string", 0),  # No string literal
#     ("\"Valid\\nString\"", 0),  # Valid escape sequence
# ]

# for test, start in test_cases:
#     result, next_index = analyzer.checking_unterminated_string(test, start)
#     print(f"Input: {test}")
#     print(f"Result: {result}")
#     print(f"Errors: {analyzer.errors}")
#     analyzer.errors.clear()  # Reset errors for the next test case
#     print("-" * 50)



