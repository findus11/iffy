from enum import Enum
from typing import Optional
import lexer as l

class Tt(l.Tt, Enum):
    NAME    = 0
    NUMBER  = 1
    STRING  = 2
    OP      = 3
    NEWLINE = 4

    def ident(lexeme: str, lexer: l.Lexer) -> Optional[l.Tt]:
        return Tt.NAME
    
    def number(lexeme: str, lexer: l.Lexer) -> Optional[l.Tt]:
        return Tt.NUMBER
    
    def string(lexeme: str, lexer: l.Lexer) -> Optional[l.Tt]:
        return Tt.STRING
    
    def op(lexeme: str, lexer: l.Lexer) -> Optional[l.Tt]:
        if lexeme == '\n':
            return Tt.NEWLINE
        return Tt.OP
