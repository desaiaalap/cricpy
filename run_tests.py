#!/usr/bin/env python
"""
Test runner script for cricpy package
Usage: python run_tests.py [options]
"""
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle output"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description='Run tests for cricpy package')
    parser.add_argument('--coverage', action='store_true', help='Run with coverage report')
    parser.add_argument('--html', action='store_true', help='Generate HTML coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--failfast', '-x', action='store_true', help='Stop on first failure')
    parser.add_argument('--parallel', '-n', type=int, help='Run tests in parallel')
    parser.add_argument('--markers', '-m', help='Run tests matching given mark expression')
    parser.add_argument('--keyword', '-k', help='Run tests matching given keyword expression')
    parser.add_argument('--module', help='Run tests for specific module only')
    parser.add_argument('--lint', action='store_true', help='Run linting checks')
    parser.add_argument('--format', action='store_true', help='Run code formatting')
    parser.add_argument('--all', action='store_true', help='Run all checks (tests, lint, format)')
    
    args = parser.parse_args()
    
    # Base test command
    test_cmd = ['pytest']
    
    # Add test directory
    test_dir = Path('cricpy/tests')
    if args.module:
        test_cmd.append(f'{test_dir}/test_{args.module}.py')
    else:
        test_cmd.append(str(test_dir))
    
    # Add options
    if args.verbose:
        test_cmd.append('-vv')
    else:
        test_cmd.append('-v')
    
    if args.failfast:
        test_cmd.append('-x')
    
    if args.parallel:
        test_cmd.extend(['-n', str(args.parallel)])
    
    if args.markers:
        test_cmd.extend(['-m', args.markers])
    
    if args.keyword:
        test_cmd.extend(['-k', args.keyword])
    
    # Coverage options
    if args.coverage or args.all:
        test_cmd.extend([
            '--cov=cricpy',
            '--cov-report=term-missing',
            '--cov-report=html:htmlcov' if args.html else '--cov-report=term'
        ])
    
    # Run tests
    return_code = 0
    
    if not args.lint and not args.format:
        return_code = run_command(test_cmd, "Unit Tests")
    
    # Run linting if requested
    if args.lint or args.all:
        # Black formatting check
        black_cmd = ['black', '--check', '--diff', 'cricpy/', 'tests/']
        lint_code = run_command(black_cmd, "Black Formatting Check")
        return_code = return_code or lint_code
        
        # Flake8 linting
        flake8_cmd = ['flake8', 'cricpy/', 'tests/', '--max-line-length=100']
        lint_code = run_command(flake8_cmd, "Flake8 Linting")
        return_code = return_code or lint_code
        
        # MyPy type checking
        mypy_cmd = ['mypy', 'cricpy/', '--ignore-missing-imports']
        lint_code = run_command(mypy_cmd, "MyPy Type Checking")
        return_code = return_code or lint_code
    
    # Run formatting if requested
    if args.format:
        # Black formatting
        black_cmd = ['black', 'cricpy/', 'tests/']
        format_code = run_command(black_cmd, "Black Formatting")
        return_code = return_code or format_code
        
        # isort import sorting
        isort_cmd = ['isort', 'cricpy/', 'tests/']
        format_code = run_command(isort_cmd, "Import Sorting")
        return_code = return_code or format_code
    
    # Summary
    print(f"\n{'='*60}")
    if return_code == 0:
        print("✅ All checks passed!")
    else:
        print("❌ Some checks failed!")
    print('='*60)
    
    return return_code


if __name__ == '__main__':
    sys.exit(main())