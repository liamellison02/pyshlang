from dataclasses import dataclass

@dataclass
class SHLError(Exception):
    """
    A custom exception class for syntax errors in the shlang language.
    
    Attributes:
        message: str - The error message
        file: str | None - The file where the error occurred
        line: int | None - The line number where the error occurred
        col_start: int | None - The starting column where the error occurred
        col_end: int | None - The ending column where the error occurred
        src_line: str | None - The source line where the error occurred
    """
    message: str
    file: str | None
    line: int | None
    col_start: int | None
    col_end: int | None
    src_line: str | None

    def __init__(self, message: str, 
                 file: str | None = None, 
                 line: int | None = None, 
                 col_start: int | None = None, 
                 col_end: int | None = None, 
                 src_line: str | None = None):
        self.message = message
        self.file = file if file is not None else None
        self.line = line if line is not None else 0
        self.col_start = col_start if col_start is not None else 0
        self.col_end = col_end if col_end is not None else col_start
        self.src_line = src_line
        super().__init__(self.message)

    def __str__(self) -> str:
        result: str = f"Error: {self.message}"

        if self.file:
            result += f"\n{self.file}: {result}"

        if self.line and self.src_line:
            result += f"\n{self.line} | {self.src_line}"

            if self.col_start:
                pointer = " " * (len(str(self.line)) + 3 + self.col_start) + "^"

                if self.col_end and self.col_end > self.col_start:
                    pointer += "~" * (self.col_end - self.col_start - 1)

                result += f"\n{pointer}-- Here."

        return result
