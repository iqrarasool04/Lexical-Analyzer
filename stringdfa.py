def dfa_cpp_string_literal(input_string):
    """
    Simulate DFA process for recognizing C++ string and character literals.
    :param input_string: The string to be validated
    :return: True if the string is valid, False otherwise.
    """
    if len(input_string) == 0:
        return False

    i = 0
    # Check if the first character is a quote (either single or double)
    if input_string[i] == '"' or input_string[i] == "'":
        i += 1
    else:
        return False

    # If it's a string literal (double quote)
    if input_string[0] == '"':
        while i < len(input_string) - 1:  # Keep processing until the closing quote
            if input_string[i] == '\\':  # Handle escape sequences
                i += 1  # Skip the escape character
                if i < len(input_string) and input_string[i] in ['n', 't', '\\', '"', "'", '0']:
                    i += 1  # Valid escape sequence
                else:
                    return False
            else:
                i += 1  # Regular character
        if input_string[i] == '"':
            return True  # Valid string literal
        else:
            return False  # Missing closing quote

    # If it's a character literal (single quote)
    elif input_string[0] == "'":
        if len(input_string) == 3 and input_string[1] != '\\' and input_string[2] == "'":
            return True  # Single character
        elif len(input_string) == 4 and input_string[1] == '\\' and input_string[2] in ['n', 't', '\\', '"', "'", '0'] and input_string[3] == "'":
            return True  # Valid escape sequence in char literal
        else:
            return False  # Invalid character literal

    return False  # Invalid literal

def test_dfa():
    test_cases = [
        '"Hello, World!"',  # Valid string literal
        "'a'",  # Valid character literal
        '"This is a string with escape \\" character."',  # Valid string with escape
        "'\\n'",  # Valid character with escape
        '"Unterminated string',  # Invalid (missing closing quote)
        "'Unterminated char",  # Invalid (missing closing quote)
        '"String with invalid escape \\z"',  # Invalid (invalid escape sequence)
        "'\\u'",  # Invalid (unrecognized escape sequence)
        "'ab'",  # Invalid (only one character allowed in char literals)
        '"Valid\\nString"',  # Valid string with escape
    ]
    
    for idx, test_case in enumerate(test_cases):
        print(f"Test case {idx + 1}: {test_case} -> {'Valid' if dfa_cpp_string_literal(test_case) else 'Invalid'}")

# Run the tests
test_dfa()


