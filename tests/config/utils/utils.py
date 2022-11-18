import argparse
import re
from importlib.metadata import distribution

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


def get_args():
    """
        Create a new ArgumentParser object. add the --help as arg!
        DOC link: https://docs.python.org/3/library/argparse.html
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='store_true')
    return parser.parse_known_args()


def get_arg_value(arg, args):
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


def parse_pytest_args(pytest_args):
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


def get_platform(pytest_args, cfg_file_session_data):
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
        capabilities = get_arg_value(arg=_CAPABILITIES_PYTEST_ARG, args=pytest_args)
        platform_match = re.search(_PLATFORM_NAME_PATTERN, capabilities)
        if platform_match:
            return platform_match.group(_PLATFORM_NAME_PATTERN_GROUP)
    if cfg_file_session_data:
        return cfg_file_session_data.get(_PLATFORM_NAME_CAPABILITY)
    raise ValueError(f'The "{_PLATFORM_NAME_CAPABILITY}" must be provided via command line or capabilities file.')


def get_project(pytest_args, cfg_file_session_data):
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
        return get_arg_value(arg=_PROJECT_PYTEST_ARG, args=pytest_args)
    if cfg_file_session_data:
        return cfg_file_session_data.get(_PROJECT_SESSION_INFO)
    raise ValueError(f'The "{_PROJECT_SESSION_INFO}" must be provided via command line or capabilities file.')
