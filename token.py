from enum import Enum
from typing import Any, Callable, Union

class Tt(Enum):
    LET          = 0
    VAR          = 1
    SET          = 2
    USE          = 3
    DO           = 4
    END          = 5
    THEN         = 6
    AND          = 7
    OR           = 8
    XOR          = 9
    NOT          = 10
    IF           = 11
    ELSE         = 12
    FOR          = 13
    ALL          = 14
    ANY          = 15
    IN           = 16
    LPAREN       = 17
    RPAREN       = 18
    PLUS         = 19
    MINUS        = 20
    STAR         = 21
    SLASH        = 22
    STAR_STAR    = 23
    EQUALS       = 24
    SLASH_EQUALS = 25
    NAME         = 26
    NUMBER       = 28
    STRING       = 29

def is_id(c: str) -> bool:
    return c.isalpha() or c.isnumeric() or c == '\'' or c == '_'

def is_id_start(c: str) -> bool:
    return c.isalpha() or c == '_'

def is_num(c: str) -> bool:
    return c.isdecimal() or c == '_' or c == '\''


class Token:
    def __init__(self, type: Tt, lit: str = "", val: Any = None) -> None:
        self.type = type
        self.lit = lit
        self.val = val

    def __str__(self) -> str:
        return str(self.lit)

    def __repr__(self) -> str:
        r = f"<Token {self.type}"
        if len(self.lit) > 0:
            r += " " + repr(self.lit)
        if self.val is not None:
            r += " " + repr(self.val)
        return r + ">"

class Lexer:
    """
    The lexer is responsible for turning a string of characters into a string of
    tokens.
    """

    class State:
        START    = 0
        FOR_QUAL = 1

    def __init__(self, src: str) -> None:
        self.src = src
        self.state = Lexer.State.START
        self.start = 0
        self.curr = 0
        self.done = False

    def id_type(self, name: str) -> Tt:
        match name, self.state:
            case "let",  _: return Tt.LET
            case "var",  _: return Tt.VAR
            case "set",  _: return Tt.SET
            case "use",  _: return Tt.USE
            case "do",   _: return Tt.DO
            case "end",  _: return Tt.END
            case "then", _: return Tt.THEN
            case "and",  _: return Tt.AND
            case "or",   _: return Tt.OR
            case "xor",  _: return Tt.XOR
            case "not",  _: return Tt.NOT
            case "if",   _: return Tt.IF
            case "else", _: return Tt.ELSE
            case "for",  _:
                self.state = Lexer.State.FOR_QUAL
                return Tt.FOR
            case "all",  Lexer.State.FOR_QUAL:
                self.state = Lexer.State.START
                return Tt.ALL
            case "any",  Lexer.State.FOR_QUAL:
                self.state = Lexer.State.START
                return Tt.ANY
            case "in",   _: return Tt.IN
        return Tt.NAME
    
    def at(self) -> Union[str, None]:
        if self.done:
            return None
        return self.src[self.curr]

    def next(self) -> Union[str, None]:
        if self.curr >= len(self.src) - 1 or self.done:
            self.curr += 1 # Ensure we get the last character
            self.done = True
            return None

        self.curr += 1
        c = self.src[self.curr]
        return c

    def sub(self) -> str:
        return self.src[self.start:self.curr]
    
    def consume(self, type: Tt, val: Any = None) -> Token:
        lit = self.sub()
        self.start = self.curr
        return Token(type, lit)
    
    def move_while(self, f: Callable[[str], bool]):
        c = self.at()
        while not self.done and f(c):
            c = self.next()

    def move_until(self, f: Callable[[str], bool]):
        c = self.at()
        while not self.done and not f(c):
            c = self.next()
    
    def skip_ws(self):
        self.move_while(lambda c: c.isspace())
        self.consume(None)
    
    def ident(self) -> Token:
        self.move_while(is_id)
        return self.consume(self.id_type(self.sub()))
    
    def number(self) -> Token:
        self.move_while(is_num)
        return self.consume(Tt.NUMBER, int(self.sub()))
