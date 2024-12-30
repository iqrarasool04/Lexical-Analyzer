import re
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
# from FAdo.fa import *

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


class LexicalAnalyzer:

    def __init__(self):

        # Token row
        self.lin_num = 1

        self.rules = [
            ('PREPROCESSOR', r'#.*'),       # Preprocessor directives like #include or #define
            ('MAIN', r'main'),          # main
            ('INT', r'int'),            # int
            ('FLOAT', r'float'),        # float
            ('DOUBLE', r'double'),      # double
            ('CHAR', r'char'),          # char
            ('BOOL', r'bool'),          # bool
            ('STRING', r'string'),      # string
            ('TRUE', r'true'),          # true
            ('FALSE', r'false'),        # false
            ('IF', r'if'),              # if
            ('ELSE', r'else'),          # else
            ('WHILE', r'while'),        # while
            ('FOR', r'for'),            # for
            ('DO', r'do'),              # do
            ('SWITCH', r'switch'),      # switch
            ('CASE', r'case'),          # case
            ('DEFAULT', r'default'),    # default
            ('BREAK', r'break'),        # break
            ('CONTINUE', r'continue'),  # continue
            ('RETURN', r'return'),      # return
            ('CLASS', r'class'),        # class
            ('PUBLIC', r'public'),      # public
            ('PRIVATE', r'private'),    # private
            ('PROTECTED', r'protected'),# protected
            ('NAMESPACE', r'namespace'),# namespace
            ('USING', r'using'),        # using
            ('NEW', r'new'),            # new
            ('DELETE', r'delete'),      # delete
            ('LBRACKET', r'\('),        # (
            ('RBRACKET', r'\)'),        # )
            ('LBRACE', r'\{'),          # {
            ('RBRACE', r'\}'),          # }
            ('LSQUARE', r'\['),         # [
            ('RSQUARE', r'\]'),         # ]
            ('COMMA', r','),            # ,
            ('PCOMMA', r';'),           # ;
            ('EQ', r'=='),              # ==
            ('NE', r'!='),              # !=
            ('LE', r'<='),              # <=
            ('GE', r'>='),              # >=
            ('OR', r'\|\|'),           # ||
            ('AND', r'&&'),             # &&
            ('ATTR', r'='),             # =
            ('LT', r'<'),               # <
            ('GT', r'>'),               # >
            ('PLUS', r'\+'),           # +
            ('MINUS', r'-'),            # -
            ('MULT', r'\*'),           # *
            ('DIV', r'\/'),            # /
            ('MOD', r'%'),              # %
            ('SCOPE', r'::'),           # ::
            ('STREAM_OUT', r'<<'),      # <<
            ('STREAM_IN', r'>>'),       # >>
            ('COMMENT', r'//.*|/\*.*?\*/'), # Comments
            ('ID', r'[a-zA-Z_]\w*'),   # Identifiers
            ('FLOAT_CONST', r'\d+(\.\d+)?([eE][+-]?\d+)?'), # Float
            ('INTEGER_CONST', r'\d+'), # Integer
            ('STRING_LITERAL', r'".*?"'), # String literals
            ('CHAR_LITERAL', r'\'.?\''), # Char literals
            ('NEWLINE', r'\n'),        # New line
            ('SKIP', r'[ \t]+'),       # Spaces and tabs
            ('MISMATCH', r'.'),         # Any other character
        ]



    def tokenize(self, code):

        tokens_join = '|'.join('(?P<%s>%s)' % x for x in self.rules)
        lin_start = 0
        lin_num = 1  # Line number

        # Lists of output for the program
        token_info = []  # List of tuples (token, lexeme, line, column)

        for match in re.finditer(tokens_join, code):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - lin_start
            if kind == 'NEWLINE':
                lin_num += 1
                lin_start = match.end()
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {lin_num}')
            else:
                token_info.append((kind, value, lin_num, column))

        return token_info

    def tokenize_with_automata(self, code):

        identifier_dfa = DFA(
            states={"q0", "q1"},
            input_symbols=set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"),
            transitions={
                "q0": {char: "q1" for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"},
                "q1": {char: "q1" for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"},
            },
            initial_state="q0",
            final_states={"q1"},
        )

        number_dfa = DFA(
            states={"q0", "q1"},
            input_symbols=set("0123456789"),
            transitions={
                "q0": {char: "q1" for char in "0123456789"},
                "q1": {char: "q1" for char in "0123456789"},
            },
            initial_state="q0",
            final_states={"q1"},
        )

        tokens = []
        i = 0
        while i < len(code):
            for dfa_name, dfa in [("IDENTIFIER", identifier_dfa), ("NUMBER", number_dfa)]:
                match = ""
                state = dfa.initial_state
                for j in range(i, len(code)):
                    if code[j] in dfa.input_symbols and state in dfa.transitions and code[j] in dfa.transitions[state]:
                        state = dfa.transitions[state][code[j]]
                        match += code[j]
                        if state in dfa.final_states:
                            tokens.append((dfa_name, match))
                            i = j + 1
                            break
                    else:
                        break
                else:
                    continue
                break
            else:
                tokens.append(("ERROR", code[i]))
                i += 1
        return tokens
    
    def build_dfa_for_keywords(self, keyword):
        dfa = keyword_dfa(keyword)
        return dfa
    
    def validate_with_dfa(self, token, dfa):
        return dfa.accepts_input(token)
    
    def print_tokens(self, tokens):
        print("Tokens:")
        for token_type, value in tokens:
            print(f"Type: {token_type}, Value: {value}")

    


if __name__ == "__main__":
    dfa = keyword_dfa("main")
    print("states:", dfa.states)
    print("input symbols:", dfa.input_symbols)
    print("transitions:", dfa.transitions)

    analyzer = LexicalAnalyzer()
    print(analyzer.validate_with_dfa('mai', dfa))

    # tokens = tokenize(sample_code)
    # print_tokens(tokens)

    # analyzer = LexicalAnalyzer()
    # tokens = analyzer.tokenize_with_automata(code)
    # for token in tokens:
    #     print(token)


# if __name__ == "__main__":
#     dfa1 = DFA(
#         states={'q0', 'q1', 'q2'},
#         input_symbols={'0', '1'},
#         transitions={
#             'q0': {'0': 'q0', '1': 'q1'},
#             'q1': {'0': 'q0', '1': 'q2'},
#             'q2': {'0': 'q2', '1': 'q1'}
#         },
#         initial_state='q0',
#         final_states={'q1'}
#     )
#     # If you want to make a change, you must create a new instance; please note
#     # that dfa1.input_parameters is always a deep copy of the input parameters for
#     # dfa1 (in other words, mutating dfa1.input_parameters will not actually mutate
#     # dfa1)
#     params = dfa1.input_parameters
#     params['final_states'] = {'q2'}
#     dfa2 = DFA(**params)
#     print(dfa2)