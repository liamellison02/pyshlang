import sys
import os


class ShlangError(Exception):
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
                # Calculate the pointer position
                pointer = " " * (len(str(self.line)) + 3 + self.col_start) + "^"
                
                # Add additional carets if the error spans multiple characters
                if self.col_end and self.col_end > self.col_start:
                    pointer += "~" * (self.col_end - self.col_start - 1)
                
                result += f"\n{pointer}-- Here."
        
        return result


class Scanner:
    def __init__(self, src, file=None):
        self.src = src
        self.tokens = []
        self.file = file
        self.line = 1
        self.current = 0
        self.start = 0
        self.source_lines = src.split('\n')

    def scan_tokens(self) -> list:
        # This is a placeholder for the actual implementation
        return self.tokens
    
    def error(self, message, line=None, col_start=None, col_end=None):
        if line is None:
            line = self.line
            
        if col_start is None:
            col_start = self.current
            
        source_line = self.source_lines[line-1] if line <= len(self.source_lines) else ""
        
        raise ShlangError(
            message=message,
            file=self.file,
            line=line,
            col_start=col_start,
            col_end=col_end,
            source_line=source_line
        )


class Token:
    def __init__(self, type, value, line, col_start, col_end=None):
        self.type = type
        self.value = value
        self.line = line
        self.col_start = col_start
        self.col_end = col_end if col_end is not None else col_start

    def __str__(self):
        return f"{self.type} {self.value} {self.line}:{self.col_start}"


def report_error(error):
    print(error, file=sys.stderr)


def run(src: str, file=None):
    try:
        scanner = Scanner(src, file)
        tokens = scanner.scan_tokens()
        print(tokens)
    except ShlangError as e:
        report_error(e)
        return 1
    return 0


def run_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            src = file.read()
        return run(src, os.path.basename(path))
    except FileNotFoundError:
        print(f"Error: Could not open file '{path}'")
        return 1


def run_prompt():
    had_error = False
    while True:
        try:
            print("> ", end="")
            line = input()
            had_error = run(line, "<stdin>") != 0
        except EOFError:
            break
    return 1 if had_error else 0


def main():
    # TODO: advanced options/flags using argparse
    if len(sys.argv) > 2:
        print("Usage: pyshlang [script]")
        return 64
    elif len(sys.argv) == 2:
        return run_file(sys.argv[1])
    else:
        return run_prompt()


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except ShlangError as e:
        report_error(e)
        sys.exit(1)
    except Exception as e:
        print(f"Internal error: {e}")
        sys.exit(1)
