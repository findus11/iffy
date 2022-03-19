from enum import Enum
from typing import Optional
import lexer as l


class State(Enum):
    FOR_QUAL = 0


class Tt(l.Tt, Enum):
    NAME = 0
    NUMBER = 1
    STRING = 2
    NEWLINE = 3

    IS = 10
    LET = 11
    VAL = 12
    VAR = 13
    SET = 14
    TYPE = 15

    RETURN = 30
    BREAK = 31
    CONTINUE = 32
    THEN = 33

    DO = 50
    END = 51
    IF = 52
    ELSE = 53
    FOR = 54
    ALL = 55
    ANY = 56
    IN = 57
    WHILE = 58

    AND = 80
    OR = 81
    XOR = 82
    NOT = 83
    MOD = 84

    LPAREN = 100
    RPAREN = 101
    LBRACKET = 102
    RBRACKET = 103
    LBRACE = 104
    RBRACE = 105

    PLUS = 110
    MINUS = 111
    STAR = 112
    SLASH = 113
    STAR_STAR = 114

    EQUALS = 120
    SLASH_EQUALS = 121
    GREATER = 122
    GREATER_EQUALS = 123
    LESS = 124
    LESS_EQUALS = 125

    def ident(lexeme: str, lexer: l.Lexer) -> Optional[l.Tt]:
        match lexeme, lexer.state:
            case "is", _: return Tt.IS
            case "let", _: return Tt.LET
            case "val", _: return Tt.VAL
            case "var", _: return Tt.VAR
            case "set", _: return Tt.SET
            case "type", _: return Tt.TYPE
            case "return", _: return Tt.RETURN
            case "break", _: return Tt.BREAK
            case "continue", _: return Tt.CONTINUE
            case "then", _: return Tt.THEN
            case "do", _: return Tt.DO
            case "end", _: return Tt.END
            case "if", _: return Tt.IF
            case "else", _: return Tt.ELSE
            case "for", _:
                lexer.state = State.FOR_QUAL
                return Tt.FOR
            case "all", State.FOR_QUAL:
                lexer.state = l.Lexer.State.START
                return Tt.ALL
            case "any", State.FOR_QUAL:
                lexer.state = l.Lexer.State.START
                return Tt.ANY
            case "in", _: return Tt.IN
            case "while", _: return Tt.WHILE
            case "and", _: return Tt.AND
            case "or", _: return Tt.OR
            case "xor", _: return Tt.XOR
            case "not", _: return Tt.NOT
            case "mod", _: return Tt.MOD
            case _: return Tt.NAME

    def number(lexeme: str, lexer: l.Lexer) -> Optional[l.Tt]:
        return Tt.NUMBER

    def string(lexeme: str, lexer: l.Lexer) -> Optional[l.Tt]:
        return Tt.STRING

    def op(lexer: l.Lexer) -> Optional[l.Tt]:
        c = lexer.curr()
        match c:
            case '\n': return Tt.NEWLINE
            case '(': return Tt.LPAREN
            case ')': return Tt.RPAREN
            case '[': return Tt.LBRACKET
            case ']': return Tt.RBRACKET
            case '{': return Tt.LBRACE
            case '}': return Tt.RBRACE
            case '+': return Tt.PLUS
            case '-': return Tt.MINUS
            case '*':
                if lexer.move_on('*'):
                    return Tt.STAR_STAR
                return Tt.STAR
            case '/':
                if lexer.move_on('='):
                    return Tt.SLASH_EQUALS
                return Tt.SLASH
            case '=': return Tt.EQUALS
            case '>':
                if lexer.move_on('='):
                    return Tt.GREATER_EQUALS
                return Tt.GREATER
            case '<':
                if lexer.move_on('='):
                    return Tt.LESS_EQUALS
                return Tt.LESS
            case _: return None
