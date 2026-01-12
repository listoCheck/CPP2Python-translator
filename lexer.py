import re


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}"


TOKEN_SPEC = [
    ('CLASS', r'class\b'),
    ('INT', r'int\b'),
    ('IF', r'if\b'),
    ('WHILE', r'while\b'),
    ('RETURN', r'return\b'),
    ('CIN', r'cin\b'),
    ('COUT', r'cout\b'),
    ('SHL', r'<<'),
    ('SHR', r'>>'),
    ('LINE_COMMENT', r'//[^\n]*'),
    ('BLOCK_COMMENT', r'/\*.*?\*/'),
    ('DIV', r'/'),
    ('NUMBER', r'\d+'),
    ('IDENT', r'[a-zA-Z_]\w*'),
    ('ASSIGN', r'='),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('SKIP', r'[ \t\n]+'),
    ('MISMATCH', r'.'),
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC)


def lexer(code):
    tokens = []
    for m in re.finditer(TOKEN_REGEX, code, re.DOTALL):
        kind = m.lastgroup
        value = m.group()
        if kind == 'SKIP':
            continue
        if kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected symbol: {value}")
        tokens.append(Token(kind, value))
    tokens.append(Token('EOF', ''))
    return tokens
