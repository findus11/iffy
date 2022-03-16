from enum import Enum
from typing import Union

class Tt(Enum):
    LET          = 0
    VAR          = 1
    SET          = 2
    USE          = 3
    DO           = 4
    END          = 5
    IF           = 6
    ELSE         = 7
    FOR          = 8
    ALL          = 9
    ANY          = 10
    IN           = 11
    LPAREN       = 12
    RPAREN       = 13
    PLUS         = 14
    MINUS        = 15
    STAR         = 16
    SLASH        = 17
    STAR_STAR    = 18
    EQUALS       = 19
    SLASH_EQUALS = 20
    IDENT        = 21
    NUMBER       = 22
    STRING       = 23

class Token:
    def __init__(self, type: Tt, lit: str = "") -> None:
        self.type = type
        self.lit = lit

    def __str__(self) -> str:
        return str(self.lit)

    def __repr__(self) -> str:
        return f"<Token {self.type} {repr(self.lit)}>"

class Lexer:
    """
    The lexer is responsible for turning a string of characters into a string of
    tokens.
    """
    def __init__(self, src) -> None:
        self.src = src
        self.start = 0
        self.curr = 0
        self.done = False

    def next(self) -> Union[chr, None]:
        if self.curr >= len(self.src) or self.done:
            self.done = True
            return None

        c = self.src[self.curr]
        self.curr += 1
        return c
