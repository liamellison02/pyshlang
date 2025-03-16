from dataclasses import dataclass
from enum import Enum, auto

from .error import SHLError

class TokenType(Enum):
    # Single-char tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()
    COLON = auto()
    EQUAL = auto()
    
    # Operators
    BANG_EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    ARROW = auto()
    
    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    
    # Keywords
    AND = auto()
    OR = auto()
    IF = auto()
    ELSE = auto()
    TRUE = auto()
    FALSE = auto()
    FOR = auto()
    WHILE = auto()
    FN = auto()
    RETURN = auto()
    VAR = auto()
    IMPORT = auto()
    IN = auto()
    BANG = auto()
    CLASS = auto()
    NIL = auto()
    DISPLAY = auto()
    READ = auto()
    EOF = auto()

@dataclass
class Token:
    """
    Attributes:
        type: The type of the token
        lexeme: The lexeme of the token
        literal: The literal value of the token
        line: The line number of the token
        col_start: The starting column of the token
        col_end: The ending column of the token
    """
    type: TokenType
    lexeme: str
    literal: Optional[object] = None
    line: int = 0
    col_start: int = 0
    col_end: int = 0
    
    def __str__(self) -> str:
        return f"Token(type={self.type}, lexeme='{self.lexeme}', line={self.line}, col={self.col_start})"

@dataclass
class Scanner:
    """ 
    Attributes:
        tokens: The tokens generated from the source code
        source: The source code to tokenize
        current: The current position in the source code
        line: The current line number
        start: The starting position of the current lexeme
        keywords: A dictionary mapping keywords to their token types
    """
    
    def __init__(self):
        self.tokens: list[Token] = []
        self.source: str = ""
        self.current: int = 0
        self.start: int = 0
        self.line: int = 1
        self.column: int = 1
        
        self._keywords: dict[str, TokenType] = {
            "and": TokenType.AND,
            "or": TokenType.OR,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "while": TokenType.WHILE,
            "fn": TokenType.FN,
            "return": TokenType.RETURN,
            "var": TokenType.VAR,
            "import": TokenType.IMPORT,
            "in": TokenType.IN,
            "class": TokenType.CLASS,
            "nil": TokenType.NIL,
            "display": TokenType.DISPLAY,
            "read": TokenType.READ,
        }
        
        self._single_char_tokens: Dict[str, TokenType] = {
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            "{": TokenType.LEFT_BRACE,
            "}": TokenType.RIGHT_BRACE,
            "[": TokenType.LEFT_BRACKET,
            "]": TokenType.RIGHT_BRACKET,
            ",": TokenType.COMMA,
            ".": TokenType.DOT,
            "-": TokenType.MINUS,
            "+": TokenType.PLUS,
            ";": TokenType.SEMICOLON,
            "/": TokenType.SLASH,
            "*": TokenType.STAR,
            ":": TokenType.COLON,
            "=": TokenType.EQUAL,
            ">": TokenType.GREATER,
            "<": TokenType.LESS,
            "!": TokenType.BANG,
        }
        
        self._two_char_tokens: Dict[str, TokenType] = {
            "!=": TokenType.BANG_EQUAL,
            "==": TokenType.EQUAL_EQUAL,
            ">=": TokenType.GREATER_EQUAL,
            "<=": TokenType.LESS_EQUAL,
            "=>": TokenType.ARROW,
        }
        
        self.reserved_chars: str = "(){}[],.;+-*/=><:!\"'"
    
    def scan_tokens(self, src: str) -> List[Token]:
        """
        Scan the source code and generate tokens.
        
        Args:
            src: The source code to scan
            
        Returns:
            A list of tokens
        """
        self.source = src
        self.tokens = []
        self.current = 0
        self.start = 0
        self.line = 1
        self.column = 1
        
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column, self.column))
        return self.tokens
    
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def scan_token(self) -> None:
        """Scan a single token."""
        c = self.advance()
        if c.isspace():
            if c == '\n':
                self.line += 1
                self.column = 1
            return
        
        if c == '/' and self.match('/'):
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()
            return
        
        if c in self._single_char_tokens:
            if c in ['!', '=', '>', '<'] and self.peek() in ['=', '>']:
                next_char = self.advance()
                two_char = c + next_char
                if two_char in self._two_char_tokens:
                    self.add_token(self._two_char_tokens[two_char])
                    return
                self.current -= 1
                self.column -= 1
            
            self.add_token(self._single_char_tokens[c])
            return
        
        if c == '"' or c == "'":
            self.string(c)
            return
        
        if c.isdigit():
            self.number()
            return
        
        if c.isalpha() or c == '_':
            self.identifier()
            return
        
        raise SHLError(f"Unexpected character: '{c}'", line=self.line, col_start=self.column - 1)
    
    def advance(self) -> str:
        """Advance the current position and return the current character."""
        c = self.source[self.current]
        self.current += 1
        self.column += 1
        return c
    
    def match(self, expected: str) -> bool:
        """Check if the current character matches the expected character."""
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        
        self.current += 1
        self.column += 1
        return True
    
    def peek(self) -> str:
        """Look at the current character without advancing."""
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
    
    def peek_next(self) -> str:
        """Look at the next character without advancing."""
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def string(self, quote: str) -> None:
        """Process a string literal."""
        while self.peek() != quote and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
                self.column = 1
            self.advance()
        
        if self.is_at_end():
            raise SHLError("Unterminated string.", line=self.line, col_start=self.column)
        
        self.advance()
        
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)
    
    def number(self) -> None:
        """Process a number literal."""
        while self.peek().isdigit():
            self.advance()
        
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            
            while self.peek().isdigit():
                self.advance()
        
        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)
    
    def identifier(self) -> None:
        """Process an identifier or keyword."""
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        
        text = self.source[self.start:self.current]
        token_type = self._keywords.get(text.lower(), TokenType.IDENTIFIER)
        
        self.add_token(token_type)
    
    def add_token(self, token_type: TokenType, literal: object = None) -> None:
        """Add a token to the list of tokens."""
        text = self.source[self.start:self.current]
        self.tokens.append(Token(
            token_type,
            text,
            literal,
            self.line,
            self.start,
            self.current
        ))
