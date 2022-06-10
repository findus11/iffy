from enum import Enum
from lexer import Token, Tt
from typing import Callable, TypeVar


class Ast:
    pass


class Parsebag:
    pass


P = TypeVar("P", bound="Parser")
ParserType = Callable[[P], Ast | None]


class Parser:
    """
    Turns a sequence of tokens (see lexer.py) into abstract syntax trees, which
    represents the source with a tree-like structure that is easier to
    manipulate.
    """

    class Step(Enum):
        DECL = 0
        STMT = 1
        EXPR = 2
        TYPE = 3

    def __init__(self, toks: list[Token]):
        self.toks = toks

        self.decl_parsers: list[tuple[Tt | None, ParserType]] = []
        self.stmt_parsers: list[tuple[Tt | None, ParserType]] = []
        self.expr_parsers: list[tuple[Tt | None, ParserType]] = []
        self.type_parsers: list[tuple[Tt | None, ParserType]] = []

    def add_pb(self, pb: Parsebag):
        pb.register(self)

    # Add some number of functions to the parser. These can be used like utility
    # functions, but won't be called automatically.
    def mixin(self, *args):
        for arg in args:
            setattr(Parser, arg.__name__, arg)

    def add_parse(self, step: Step, parse: ParserType, *, on: Tt | None = None):
        match step:
            case Parser.Step.DECL: self.decl_parsers.append((on, parse))
            case Parser.Step.STMT: self.stmt_parsers.append((on, parse))
            case Parser.Step.EXPR: self.expr_parsers.append((on, parse))
            case Parser.Step.TYPE: self.type_parsers.append((on, parse))
            case _: raise Exception("expected one of DECL, STMT, EXPR or TYPE for step")

    def expect(self, tt: Tt | list[Tt], err: str = ""):
        NotImplemented

    def parse_decl() -> Ast:
        NotImplemented

    def parse_stmt() -> Ast:
        NotImplemented

    def parse_expr() -> Ast:
        NotImplemented

    def parse_type() -> Ast:
        NotImplemented
