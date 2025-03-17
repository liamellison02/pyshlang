from dataclasses import dataclass

from .scanner import Scanner, TokenType, Token
from .error import SHLError
from .parser import Parser

__all__ = [
    "Parser",
    "Scanner",
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
        scanner: The scanner used to tokenize the source code
        src_path: The path to the source code file
    """
    scanner: Scanner
    src_path: str | None

    def __init__(self, src_path: str | None = None):
        self.scanner = Scanner()
        self.src_path = src_path

    def run(self, src: str | None = None):
        """
        Run the pyshlang interpreter.
        
        Args:
            src: The source code to run
        """
        if src is None:
            return

        for token in self.scanner.scan_tokens(src):
            print(f"{token}\n")
            
    # TODO: implement run_prompt
    def run_prompt(self) -> None:
        raise NotImplementedError
