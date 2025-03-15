import sys
import argparse
from utils import PyShlang, SHLError

__version__ = "0.1.0"

def main() -> None:
    """
    Main entry point for the pyshlang interpreter.
    Parses command line arguments and runs the interpreter accordingly.
    """
    parser = argparse.ArgumentParser(
        prog="pyshlang",
        description="pyshlang - A simple interpreter for the SHLang language"
    )
    parser.add_argument(
        "script",
        nargs="?",
        help="Path to the script file to execute"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"pyshlang {__version__}",
        help="Show version and exit"
    )

    args = parser.parse_args()
    pyshlang = PyShlang(src_path=args.script)

    if args.script:
        with open(args.script, 'r') as f:
            source = f.read()
        pyshlang.run(source)
    else:
        pyshlang.run_prompt()


if __name__ == "__main__":
    print(f"""<pyshlang v{__version__}>\n\nWell here goes nothing...\n\n""")
    try:
        main()
    except SHLError as e:
        print(e)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: Could not open file: {e}")
        sys.exit(2)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt. Exiting...")
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    sys.exit(0)
