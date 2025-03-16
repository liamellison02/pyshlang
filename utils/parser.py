from dataclasses import dataclass
from enum import Enum, auto

from utils.lexer import Token

class ExprType(Enum):
    UNARY = auto()
    BINARY = auto()
    GROUPING = auto()
    LITERAL = auto()    

@dataclass
class AST:
    pass

@dataclass
class Parser: 
    pass