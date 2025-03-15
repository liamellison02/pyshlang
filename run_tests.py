#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import time
import re
import json

# ANSI color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def find_test_files(test_dir: str, pattern: Optional[str] = None) -> List[Path]:
    """
    Find all test files in the specified directory.
    
    Args:
        test_dir: Directory containing test files
        pattern: Optional regex pattern to filter test files
    
    Returns:
        List of Path objects for the test files
    """
    test_dir_path = Path(test_dir)
    if not test_dir_path.exists() or not test_dir_path.is_dir():
        print(f"Error: Test directory {test_dir} does not exist")
        sys.exit(1)
    
    test_files = list(test_dir_path.glob("*.shl"))
    
    if pattern:
        regex = re.compile(pattern)
        test_files = [f for f in test_files if regex.search(f.name)]
    
    if not test_files:
        print(f"No test files found in {test_dir}" + 
              (f" matching pattern '{pattern}'" if pattern else ""))
        sys.exit(1)
    
    return sorted(test_files)

def get_expected_statuses(path: Optional[str] = None) -> Dict[str, bool]:
    """
    Get the expected status for each test file.
    
    Args:
        path: Path to the JSON file containing expected statuses
    
    Returns:
        Dictionary mapping test file names to expected success status
    """
    if path is None:
        path = Path(__file__).parent / "expected_test_results.json"
    
    if Path(path).exists():
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"{YELLOW}Warning: Could not parse expected test results file. Using default expectations.{RESET}")
    
    return {}

def save_expected_statuses(expected_statuses: Dict[str, bool], path: Optional[str] = None) -> None:
    """
    Save the expected statuses for future test runs.
    
    Args:
        expected_statuses: Dictionary mapping test file names to expected success status
        path: Path to save the JSON file
    """
    if path is None:
        path = Path(__file__).parent / "expected_test_results.json"
    
    with open(path, 'w') as f:
        json.dump(expected_statuses, f, indent=4)

def run_test(test_file: Path, interpreter_path: str, verbose: bool) -> Tuple[bool, str, float]:
    """
    Run a single test file through the interpreter.
    
    Args:
        test_file: Path to the test file
        interpreter_path: Path to the Shlang interpreter
        verbose: Whether to print the test output
    
    Returns:
        Tuple of (success, output, execution_time)
    """
    if verbose:
        print(f"{CYAN}Running test file: {test_file}{RESET}")
    
    start_time = time.time()
    try:
        # Run the interpreter with the test file
        result = subprocess.run(
            [interpreter_path, str(test_file)],
            capture_output=True,
            text=True,
            check=False,
            timeout=10  # Add a timeout to prevent hanging tests
        )
        execution_time = time.time() - start_time
        
        # Check if the command executed successfully
        if result.returncode == 0:
            return True, result.stdout, execution_time
        else:
            # Combine stdout and stderr for better diagnostics
            output = ""
            if result.stdout.strip():
                output += f"STDOUT:\n{result.stdout.strip()}\n\n"
            if result.stderr.strip():
                output += f"STDERR:\n{result.stderr.strip()}"
            
            return False, f"Error (exit code {result.returncode}):\n{output}", execution_time
    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        return False, "Test timed out after 10 seconds", execution_time
    except Exception as e:
        execution_time = time.time() - start_time
        return False, f"Exception occurred: {str(e)}", execution_time

def print_test_result(test_name: str, success: bool, expected_success: Optional[bool], 
                    output: str, execution_time: float, verbose: bool):
    """Print the result of a test."""
    if expected_success is not None:
        # Test behavior matches expectations
        if success == expected_success:
            if success:
                status = f"{GREEN}✓ PASS{RESET}"
            else:
                status = f"{YELLOW}✗ EXPECTED FAIL{RESET}"
        # Test behavior doesn't match expectations
        else:
            if success:
                status = f"{BLUE}✓ UNEXPECTED PASS{RESET}"
            else:
                status = f"{RED}✗ FAIL{RESET}"
    else:
        # No expectations set
        status = f"{GREEN}✓ PASS{RESET}" if success else f"{RED}✗ FAIL{RESET}"
    
    print(f"{status} {test_name} ({execution_time:.3f}s)")
    
    if verbose or (expected_success is None and not success) or (expected_success is not None and success != expected_success):
        if output.strip():
            print(f"\n{BLUE}Output:{RESET}")
            print(f"{output.strip()}")
            print(f"{'-' * 40}\n")

def analyze_error_patterns(results: Dict[Path, Tuple[bool, str, float]]) -> Dict[str, int]:
    """
    Analyze error patterns across failed tests.
    
    Args:
        results: Test results
    
    Returns:
        Dictionary mapping error patterns to counts
    """
    error_patterns = {}
    for _, (success, output, _) in results.items():
        if not success:
            # Extract key error messages
            error_lines = []
            for line in output.splitlines():
                if "Error:" in line or "Exception:" in line:
                    error_lines.append(line.strip())
            
            if error_lines:
                key_error = error_lines[-1]  # Use the last error line as key
                error_patterns[key_error] = error_patterns.get(key_error, 0) + 1
    
    return error_patterns

def main():
    parser = argparse.ArgumentParser(description="Run Shlang tests")
    parser.add_argument(
        "-d", "--test-dir",
        default="tests",
        help="Directory containing test files (default: tests)"
    )
    parser.add_argument(
        "-i", "--interpreter",
        default="./shlang",
        help="Path to the Shlang interpreter (default: ./shlang)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print detailed output for all tests"
    )
    parser.add_argument(
        "-p", "--pattern",
        help="Regex pattern to filter test files"
    )
    parser.add_argument(
        "-e", "--expected-results",
        help="Path to JSON file with expected test results"
    )
    parser.add_argument(
        "-u", "--update-expectations",
        action="store_true",
        help="Update expected test results based on current run"
    )
    parser.add_argument(
        "--allow-failure",
        action="store_true",
        help="Exit with status code 0 even if tests fail"
    )
    
    args = parser.parse_args()
    
    # Find test files
    test_files = find_test_files(args.test_dir, args.pattern)
    
    # Load expected statuses
    expected_statuses = get_expected_statuses(args.expected_results)
    
    # Print header
    print(f"\n{BOLD}Running {len(test_files)} Shlang tests{RESET}\n")
    
    # Run tests
    results: Dict[Path, Tuple[bool, str, float]] = {}
    for test_file in test_files:
        success, output, execution_time = run_test(test_file, args.interpreter, args.verbose)
        results[test_file] = (success, output, execution_time)
        
        expected_success = expected_statuses.get(test_file.name)
        print_test_result(test_file.name, success, expected_success, output, execution_time, args.verbose)
        
        # Update expected statuses if requested
        if args.update_expectations:
            expected_statuses[test_file.name] = success
    
    # Save updated expected statuses if requested
    if args.update_expectations:
        save_expected_statuses(expected_statuses, args.expected_results)
        print(f"\n{YELLOW}Updated expected test results{RESET}")
    
    # Print summary
    passed = sum(1 for success, _, _ in results.values() if success)
    failed = len(results) - passed
    expected_to_fail = sum(1 for test_file in test_files if not expected_statuses.get(test_file.name, True))
    total_time = sum(execution_time for _, _, execution_time in results.values())
    
    print(f"\n{BOLD}Test Summary:{RESET}")
    print(f"Total: {len(results)} | {GREEN}Passed: {passed}{RESET} | {RED}Failed: {failed}{RESET}")
    if expected_to_fail > 0:
        print(f"Expected failures: {expected_to_fail}")
    print(f"Total execution time: {total_time:.3f}s")
    
    # Analyze error patterns if there are failures
    if failed > 0:
        error_patterns = analyze_error_patterns(results)
        if error_patterns:
            print(f"\n{BOLD}Common Error Patterns:{RESET}")
            for error, count in sorted(error_patterns.items(), key=lambda x: x[1], reverse=True):
                print(f"{count} tests: {error}")
    
    # Exit with appropriate status code
    if args.allow_failure:
        sys.exit(0)
    else:
        # Exit with success if all test results match expectations
        unexpected_failures = sum(1 for file, (success, _, _) in results.items() 
                                if not success and expected_statuses.get(file.name, True))
        sys.exit(0 if unexpected_failures == 0 else 1)

if __name__ == "__main__":
    main()
