import sys


def run(source):
    # Process the source code
    # This is a placeholder for the actual implementation
    print(source)


def run_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        source = file.read()
    run(source)


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
    main()