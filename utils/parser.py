from dataclasses import dataclass
from enum import Enum, auto

from .scanner import Token, TokenType
from .error import SHLError

class SyntaxError(SHLError):
    pass


class ExprType(Enum):
    UNARY = auto()
    BINARY = auto()
    GROUPING = auto()
    LITERAL = auto()    

@dataclass
class AST:
    pass

class Parser:
    def parse(self, tokens: list[Token]) -> AST:
        pass
