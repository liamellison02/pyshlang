from dataclasses import dataclass

from .lexer import Lexer, TokenType, Token
from .error import SHLError

__all__ = [
    "Lexer",
    "TokenType",
    "Token",
    "SHLError",
    "PyShlang"
]

@dataclass
class PyShlang:
    """
    A wrapper class for the pyshlang interpreter.
    
    Attributes:
        lexer: The lexer used to tokenize the source code
        src_path: The path to the source code file
    """
    lexer: Lexer
    src_path: str | None

    def __init__(self, src_path: str | None = None):
        self.lexer = Lexer()
        self.src_path = src_path

    def run(self, src: str | None = None):
        """
        Run the pyshlang interpreter.
        
        Args:
            src: The source code to run
        """
        if src is None:
            return

        for token in self.lexer.scan_tokens(src):
            print(f"{token}\n")

    # TODO: implement run_prompt
    def run_prompt(self) -> None:
        raise NotImplementedError
