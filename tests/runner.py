import argparse
import os
import sys
import pytest


def _get_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='store_true')
    return parser.parse_known_args()[1]


def main():
    pytest_args = _get_args()
    tests_path = f'{os.path.dirname(os.path.abspath(__file__))}'
    # Pytest commands: https://gist.github.com/amatellanes/12136508b816469678c2
    pytest_command = [
        '--verbose',
        '--capture=tee-sys',  # https://docs.pytest.org/en/6.2.x/capture.html
        '-rA',  # Terminal Summary, more information: https://docs.pytest.org/en/latest/how-to/output.html
        '--tb=short',  # Terminal Summary, short result: https://docs.pytest.org/en/latest/how-to/output.html
        '--log-cli-level=10',  # Terminal Color
        tests_path,
        '-W ignore::UserWarning',  # Ignore Warnings, more information: https://docs.pytest.org/en/6.2.x/warnings.html
        '--color=yes'  # Terminal Color
    ]
    exit_code = pytest.main([*pytest_command, *pytest_args])
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
