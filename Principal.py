#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Buffer import Buffer
from LexicalAnalyzer import LexicalAnalyzer

if __name__ == '__main__':
    buffer = Buffer()  # Use lowercase for variable names (PEP 8 convention)
    analyzer = LexicalAnalyzer()

    # Lists for storing tokens, lexemes, row numbers, and column numbers
    token = []
    lexeme = []
    row = []
    column = []

    # Tokenize and reload the buffer
    for i in buffer.load_buffer():
        # Now tokenize returns a list of tuples, so we need to unpack each tuple
        for t, lex, lin, col in analyzer.tokenize(i):
            token.append(t)     # Add token to the list
            lexeme.append(lex)  # Add lexeme to the list
            row.append(lin)     # Add line number to the list
            column.append(col)  # Add column number to the list

    # Print the recognized tokens and lexemes with their line and column numbers
    print('\nRecognized Tokens: ', token)
    print('Lexemes: ', lexeme)
    print('Rows: ', row)
    print('Columns: ', column)

