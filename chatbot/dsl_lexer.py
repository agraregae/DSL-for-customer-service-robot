import re
from typing import List, Tuple

Token = Tuple[str, str]  # (token_type, token_value)


class DSLLexer:
    token_specification = [
        ("BOT", r'bot'),
        ("INTENT", r'intent'),
        ("DEFAULT", r'default'),
        ("SAY", r'say'),
        ("ASK", r'ask'),
        ("SET", r'set'),
        ("END", r'end'),
        ("AS", r'as'),

        ("STRING", r'"[^"]*"'),
        ("IDENT", r'[A-Za-z_][A-Za-z0-9_]*'),
        ("LBRACE", r'\{'),
        ("RBRACE", r'\}'),
        ("EQUAL", r'='),

        ("NEWLINE", r'\n'),
        ("SKIP", r'[ \t]+'),
        ("COMMENT", r'\#.*'),
    ]

    def __init__(self):
        parts = []
        for name, pattern in self.token_specification:
            parts.append(f'(?P<{name}>{pattern})')

        self.master_pattern = re.compile("|".join(parts))

    def tokenize(self, code: str) -> List[Token]:
        tokens: List[Token] = []
        for mo in self.master_pattern.finditer(code):
            kind = mo.lastgroup
            value = mo.group()

            if kind == "NEWLINE" or kind == "SKIP" or kind == "COMMENT":
                continue

            if kind == "STRING":
                value = value[1:-1]  # 去掉两侧引号

            tokens.append((kind, value))

        return tokens
