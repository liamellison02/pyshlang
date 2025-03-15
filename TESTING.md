# Testing Shlang Interpreter

This document provides guidelines for testing the Shlang interpreter.

## Test Runner Script

The `run_tests.py` script allows you to run all Shlang test files and validate the interpreter functionality. The script runs all `.shl` test files in the test directory to validate the interpreter.

### Usage

```bash
# Run all tests
./run_tests.py

# Run tests with verbose output
./run_tests.py -v

# Run tests matching a specific pattern
./run_tests.py -p "Loop"

# Specify a different test directory
./run_tests.py -d custom_tests

# Specify a different interpreter path
./run_tests.py -i /path/to/custom/shlang
```

### Command Line Options

- `-d, --test-dir`: Directory containing test files (default: tests)
- `-i, --interpreter`: Path to the Shlang interpreter (default: ./shlang)
- `-v, --verbose`: Print detailed output for all tests
- `-p, --pattern`: Regex pattern to filter test files

### Output

The test runner provides:

- Color-coded pass/fail indicators for each test
- Execution time for each test
- Error output for failed tests
- A summary of the total tests run, passed, and failed

### Exit Codes

- `0`: All tests passed
- `1`: At least one test failed

## Writing Tests

When writing new tests for the Shlang interpreter:

1. Create a new `.shl` file in the tests directory with a descriptive name (e.g., `test_Feature.shl`)
2. Write Shlang code that tests the specific feature
3. Use the `main()` function as the entry point into your test file.
4. Make sure to include meaningful assertions and outputs to verify functionality

## Contributing Tests

When contributing new tests:

1. Ensure your test file has a clear descriptive name
2. Include a brief comment at the top explaining what the test covers
3. Make sure your test produces deterministic output
4. Run your test using the test runner to verify it works correctly
5. Include your test file in any pull requests that modify the functionality it tests
