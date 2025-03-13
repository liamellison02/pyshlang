import sys
import os
from enum import Enum
import typing


class TokenType(Enum):
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    COMMA = "COMMA"
    DOT = "DOT"
    MINUS = "MINUS"
    PLUS = "PLUS"
    SEMICOLON = "SEMICOLON"
    SLASH = "SLASH"
    STAR = "STAR"
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FUN = "FUN"
    FOR = "FOR"
    GLOBAL = "GLOBAL"
    IF = "IF"
    INT = "INT"
    IN = "IN"
    LOCAL = "LOCAL"
    NIL = "NIL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WALRUS = "WALRUS"
    WHILE = "WHILE"
    EOF = "EOF"


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: typing.Any, line: int):
        self.type: TokenType = type
        self.lexeme: str = lexeme
        self.literal: typing.Any = literal
        self.line: int = line

    def __str__(self):
        return f"{self.type.name} {self.lexeme} {self.literal} {self.line}"


class SHLError(Exception):
    def __init__(self, message, file=None, line=None, col_start=None, col_end=None, source_line=None):
        self.message = message
        self.file = file
        self.line = line
        self.col_start = col_start
        self.col_end = col_end if col_end is not None else col_start
        self.source_line = source_line
        super().__init__(self.message)

    def __str__(self):
        result = f"Error: {self.message}"

        if self.file:
            result = f"{self.file}: {result}"

        if self.line is not None and self.source_line:
            result += f"\n{self.line} | {self.source_line}"

            if self.col_start is not None:
                pointer = " " * (len(str(self.line)) + 3 + self.col_start) + "^"

                if self.col_end and self.col_end > self.col_start:
                    pointer += "~" * (self.col_end - self.col_start - 1)

                result += f"\n{pointer}-- Here."

        return result


class Scanner:
    def __init__(self, src, file=None):
        self.src: str = src
        self.tokens: list[Token] = []

    def scan_tokens(self) -> list:
        return self.tokens


def run(src: str):
    scanner = Scanner(src)
    tokens = scanner.scan_tokens()
    print(tokens)


def run_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        src = file.read()
    run(src)


def run_prompt():
    while True:
        try:
            print("> ", end="")
            line = input()
            run(line)
        except EOFError:
            break


def main():
    # TODO: advanced options/flags using argparse
    if len(sys.argv) > 2:
        print("Usage: pyshlang [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
