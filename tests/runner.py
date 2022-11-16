""" Pytest script runner """
import argparse
import json
import os
import re
import sys
from glob import glob
from importlib.metadata import distribution

import ntpath
import pytest

# Args
_CAPABILITIES_PYTEST_ARG = '--capabilities'
_CONFIG_FILE_PYTEST_ARG = '--config-file'
_PROJECT_PYTEST_ARG = '--project'
_ARG_SEPARATOR = '='
_OPTIONAL_ARG_PREFIX = '-'

# Caps
_PLATFORM_NAME_CAPABILITY = 'platformName'

# Session info
_SESSION_INFO_CONFIG = 'session'
_PROJECT_SESSION_INFO = 'project'

# Platforms
_MOBILE_PLATFORMS = ('android', 'ios')

# Patterns
_PLATFORM_NAME_PATTERN_GROUP = 'platform'
_PLATFORM_NAME_PATTERN = rf'{_PLATFORM_NAME_CAPABILITY}=(?P<{_PLATFORM_NAME_PATTERN_GROUP}>\w+)'

# Folders
_MOBILE_FOLDER = 'mobile'
_WEB_FOLDER = 'web'
_TESTS_FOLDER = 'tests'


def _get_args():
    """
        Create a new ArgumentParser object. add the --help as arg!
        DOC link: https://docs.python.org/3/library/argparse.html
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='store_true')
    return parser.parse_known_args()


def _get_arg_value(arg, args):
    """

    Args:
        arg: str
            Name/key of the argument this method should return the value
        args: list
            A list of args received as parameter passed by command line
    Returns: str
        Return the value related to the arg received as a parameter
    """
    try:
        value = args[args.index(arg) + 1]
    except IndexError:
        raise ValueError(f'The provided parameter "{arg}" has no value.') from IndexError
    else:
        if value.startswith(_OPTIONAL_ARG_PREFIX):  # No value provided,
            raise ValueError(f'The provided parameter "{arg}" requires a value.') from IndexError
        return value


def _parse_pytest_args(pytest_args):
    """
        Split the parameters passed using the =, e.g: -m="login"
    Args:
        pytest_args: list
            A list of args received as parameter passed by command line
    Returns: list
         A list of args received as parameter passed by command line without = operator
    """
    parsed_pytest_args = []
    for pytest_arg in pytest_args:
        # Supporting Pytest args that contains "="
        if pytest_arg.startswith(_OPTIONAL_ARG_PREFIX) and _ARG_SEPARATOR in pytest_arg:
            parsed_pytest_arg = pytest_arg.split(_ARG_SEPARATOR, 1)
            parsed_pytest_args.extend(parsed_pytest_arg)
        else:
            parsed_pytest_args.append(pytest_arg)
    return parsed_pytest_args


def _get_platform(pytest_args, cfg_file_session_data):
    """
        Get platform
    Args:
        pytest_args: dict
            A list of args received as parameter passed by command line
        cfg_file_session_data: list
            The dict of session data, the same session data from session of capabilities_***.json

    Returns: str
        The platform value, e.g: web, android ...
    """
    if _CAPABILITIES_PYTEST_ARG in pytest_args:
        capabilities = _get_arg_value(arg=_CAPABILITIES_PYTEST_ARG, args=pytest_args)
        platform_match = re.search(_PLATFORM_NAME_PATTERN, capabilities)
        if platform_match:
            return platform_match.group(_PLATFORM_NAME_PATTERN_GROUP)
    if cfg_file_session_data:
        return cfg_file_session_data.get(_PLATFORM_NAME_CAPABILITY)
    raise ValueError(f'The "{_PLATFORM_NAME_CAPABILITY}" must be provided via command line or capabilities file.')


def _get_project(pytest_args, cfg_file_session_data):
    """
    Get the project name
    Args:
        pytest_args: list
             A list of args received as parameter passed by command line
        cfg_file_session_data:
            The dict of session data, the same session data from session of capabilities_***.json
    Returns:str
        The project name
    """
    if _PROJECT_PYTEST_ARG in pytest_args:
        return _get_arg_value(arg=_PROJECT_PYTEST_ARG, args=pytest_args)
    if cfg_file_session_data:
        return cfg_file_session_data.get(_PROJECT_SESSION_INFO)
    raise ValueError(f'The "{_PROJECT_SESSION_INFO}" must be provided via command line or capabilities file.')


def _load_config_file_session_data(pytest_args):
    """
    Load the config file session data / capabilities_***.json
    Args:
        pytest_args: list
            A list of args received as parameter passed by command line
    Returns: dict
        The dict related to session of the session data / capabilities_***.json
    """
    if _CONFIG_FILE_PYTEST_ARG in pytest_args:
        config_file = _get_arg_value(arg=_CONFIG_FILE_PYTEST_ARG, args=pytest_args)
        try:
            with open(config_file, encoding='utf8') as f:
                config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f'The file "{config_file}" provided by the parameter "{_CONFIG_FILE_PYTEST_ARG}" '
                                    f'does not exist.') from FileNotFoundError
        else:
            return config[_SESSION_INFO_CONFIG]
    return {}


def _get_tests_root_path(pytest_args, project_tests_path, cfg_file_session_data):
    """
    Get the tests root path, path of the package that store features, steps, conftest, ....
    Args:
        pytest_args: list
            A list of args received as parameter passed by command line
        project_tests_path:  str
        cfg_file_session_data: dict
            The dict of session data, the same session data from session of capabilities_***.json

    Returns: str
        Path of tests(features, steps, config,...), e.g:
        /<LOCAL>/b2b-automation-front-e2e/projects/application/application/tests/web
    """
    platform = _get_platform(pytest_args=pytest_args, cfg_file_session_data=cfg_file_session_data)
    # First checking for platform specific folders (web, android and ios)
    tests_root_path = glob(os.path.join(project_tests_path, '**', platform), recursive=True)
    if tests_root_path:
        return tests_root_path[0]
    if platform in _MOBILE_PLATFORMS:
        # Then checking for mobile folder
        tests_root_path = glob(os.path.join(project_tests_path, '**', _MOBILE_FOLDER), recursive=True)
        if tests_root_path:
            return tests_root_path[0]
    return project_tests_path


def main():
    args, pytest_args = _get_args()
    if not (args.help or pytest_args):
        print('A script for collecting and running tests within a project using pytest.\n'
              'To check the possible execution parameters, run the command:\n\n'
              'run-test-suite --help')
        return
    tests_path = f'{os.path.dirname(os.path.abspath(__file__))}'
    # Pytest commands: https://gist.github.com/amatellanes/12136508b816469678c2
    pytest_caps = [
        '--verbose',
        '--capture=tee-sys',  # https://docs.pytest.org/en/6.2.x/capture.html
        '-rA',  # Terminal Summary, more information: https://docs.pytest.org/en/latest/how-to/output.html
        '--tb=short',  # Terminal Summary, short result: https://docs.pytest.org/en/latest/how-to/output.html
        '--log-cli-level=INFO',  # Terminal Color
        '-W ignore::UserWarning',  # Ignore Warnings, more information: https://docs.pytest.org/en/6.2.x/warnings.html
        '--color=yes'  # Terminal Color
    ]
    try:
        parsed_pytest_args = _parse_pytest_args(pytest_args=pytest_args)
        pytest_caps += parsed_pytest_args
    except ValueError:
        if not args.help:
            raise
    if args.help:
        exit_code = pytest.main([*pytest_caps, '--help'])
    else:
        reporting_args = ['--html', 'report.html', '--self-contained-html'] if '--html' not in pytest_args else []
        exit_code = pytest.main([*pytest_caps, tests_path, *reporting_args])
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
