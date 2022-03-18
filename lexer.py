from enum import Enum
from importlib import import_module
from span import Span
from typing import Any, Callable, Optional

class Tt:
    pass

def is_ws(c: str) -> bool:
    return c.isspace() and c != '\n'

def is_id(c: str) -> bool:
    return c.isalpha() or c.isnumeric() or c == '\'' or c == '_'

def is_id_start(c: str) -> bool:
    return c.isalpha() or c == '_' or c =='\''

def is_num(c: str) -> bool:
    return c.isdecimal() or c == '_' or c == '\''

class UnknownTokenError(Exception):
    def __init__(self, type: str, lexeme: str):
        self.type = type
        self.lexeme = lexeme
    
    def __str__(self) -> str:
        return f"unknown {self.type}: {repr(self.lexeme)}"

class Token:
    def __init__(self, type: Tt, span: Span, lit: str = "", val: Any = None):
        self.type = type
        self.lit = lit
        self.span = span
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
    The lexer is responsible for turning a string of characters into a series of
    easily parseable tokens.
    """

    class State(Enum):
        START    = 0
        FOR_QUAL = 1
        ESCAPE   = 2

    def __init__(self, src: str):
        self.src = src
        self.state = Lexer.State.START
        self.start = 0
        self.currn = 0
        self.done = False

        self.idents: Callable[[str, Lexer], Tt] = []
        self.numbers: Callable[[str, Lexer], Tt] = []
        self.strings: Callable[[str, Lexer], Tt] = []
        self.ops: Callable[[str, Lexer], Tt] = []

    def refeed(self, new_src: str):
        self.src = new_src
        self.start = 0
        self.currn = 0
        self.done = False

    def add_tt(self, tt: Tt):
        self.idents.append(tt.ident)
        self.numbers.append(tt.number)
        self.strings.append(tt.string)
        self.ops.append(tt.op)
    
    def id_type(self, lexeme: str) -> Tt:
        for ident in reversed(self.idents):
            tt = ident(lexeme, self)
            if tt is not None:
                return tt
        raise UnknownTokenError("identifier", lexeme)
    
    def num_type(self, lexeme: str) -> Tt:
        for number in reversed(self.numbers):
            tt = number(lexeme, self)
            if tt is not None:
                return tt
        raise UnknownTokenError("number", lexeme)
    
    def str_type(self, lexeme: str) -> Tt:
        for string in reversed(self.strings):
            tt = string(lexeme, self)
            if tt is not None:
                return tt
        raise UnknownTokenError("string", lexeme)

    def op_type(self, lexeme) -> Tt:
        for op in reversed(self.ops):
            tt = op(lexeme, self)
            if tt is not None:
                return tt
        raise UnknownTokenError("operator", lexeme)
    
    def curr(self) -> Optional[str]:
        if self.done:
            return None
        return self.src[self.currn]
    
    def next(self) -> Optional[str]:
        if self.currn >= len(self.src) - 1 or self.done:
            self.currn += 1
            self.done = True
            return None
        
        self.currn += 1
        return self.src[self.currn]
    
    def peek(self) -> Optional[str]:
        if self.currn >= len(self.src) - 1 or self.done:
            return None
        return self.src[self.currn + 1]
    
    def sub(self) -> str:
        return self.src[self.start:self.currn]

    def consume(self, type: Tt, val: Any = None) -> Token:
        lit = self.sub()
        span = Span(self.start, self.currn)
        self.start = self.currn
        return Token(type, span, lit, val)
    
    def move_while(self, f: Callable[[str], bool]):
        c = self.curr()
        while not self.done and f(c):
            c = self.next()
    
    def skip_ws(self):
        self.move_while(is_ws)
        self.consume(None)

    def ident(self) -> Token:
        self.move_while(is_id)
        return self.consume(self.id_type(self.sub()))
    
    def number(self) -> Token:
        self.move_while(is_num)
        lit = self.sub()
        return self.consume(self.num_type(lit), int(lit))

    def string(self) -> Token:
        c = self.next()
        val = ""
        while not self.done:
            if self.state != Lexer.State.ESCAPE:
                if c == '"':
                    break
                if c == '\\':
                    self.state = Lexer.State.ESCAPE
                    c = self.next()
                    continue
            else:
                self.state = Lexer.State.START
                match c:
                    case 'n':  val += '\n'
                    case 'r':  val += '\r'
                    case c:    val += c
                c = self.next()
                continue

            val += c
            c = self.next()
        
        # Consume the final "
        self.next()
        return self.consume(self.str_type(self.sub()), val)
    
    def op(self) -> Token:
        self.move_while(lambda c: 
            not (is_ws(c) or is_id(c) or is_num(c) or c == '"')
        )
        return self.consume(self.op_type(self.sub()))
    
    def line_comment(self):
        self.move_while(lambda c: c != '\n')
        self.consume(None)
    
    def lex(self) -> list[Token]:
        res = []
        while not self.done:
            self.skip_ws()
            c = self.curr()
            if c is None:
                break

            if c == '-' and self.peek() == '-':
                self.line_comment()
                continue
            if is_id_start(c):
                res.append(self.ident())
                continue
            if is_num(c):
                res.append(self.number())
                continue
            if c == '"':
                res.append(self.string())
                continue

            res.append(self.op())
        return res

if __name__ == "__main__":
    print("Ctrl+D to exit, `--plug <module>` to add plugin")
    l = Lexer("")

    while True:
        query: str
        
        try:
            query = input("> ")
        except EOFError:
            print()
            break

        if query.startswith("--plug"):
            if len(query.split()) < 2:
                print("usage: --plug <module>")
                continue
            try:
                module = query.split()[1]
                plug = import_module(module)
                l.add_tt(plug.Tt)
            except Exception as e:
                print(e)

            continue

        l.refeed(query)
        res: list[Token]
        try:
            res = l.lex()
        except Exception as e:
            print(e)
            continue
        print(res)

