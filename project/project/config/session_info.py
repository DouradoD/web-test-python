import json
from dataclasses import dataclass
from datetime import datetime

from .constants import (SessionKeys, Capabilities, CommandExecutor, Platform, Browser, SUPPORTED_MOBILE_PLATFORMS,
                        PROJECT_ENTRY_POINT_TAG, BROWSERSTACK_BUILD_NAME_PATTERN, APPIUM_V1_22_0)
from .logger import logger

_SESSION_CONFIG_FILE_KEY = 'session'
_CAPABILITIES_CONFIG_FILE_KEY = 'capabilities'
_CMD_LINE_SOURCE = 'command line (function call arguments)'
_CONFIG_FILE_SOURCE = 'config file'
_ARGUMENT_SOURCE_LOG_PATTERN = 'Argument: "{key}", source: "{source}", value: "{value}".'
_CAPABILITY_SOURCE_LOG_PATTERN = 'Capability: "{key}", source: "{source}", value: "{value}".'
# HEADLESS CAPABILITIES
_CHROME_CAP_HEADLESS = {Capabilities.CHROME_ARGS.value: ['--headless', 'window-size=1920x1080']}
_FIREFOX_CAP_HEADLESS = {Capabilities.FIREFOX_ARGS.value: ['-headless']}
# Flutter capabilities
_FLUTTER_AUTOMATION_NAME = 'Flutter'


class InvalidRemoteArgumentException(TypeError):
    """ Exception raised when there is an error on Remote parameterization.

    Raised when invalid type (including empty - None) arguments are provided to instantiate the Remote object.

    """


class PlatformNotSupportedException(Exception):
    """ Exception raised when platform under test is not supported by the framework. """


@dataclass
class SessionInfo:
    """ The class to contain all session info. """
    platform: str = None
    project: str = None
    environment: str = None
    zone: str = None
    partner: str = None
    browserstack: bool = None
    browserstack_user: str = None
    browserstack_key: str = None
    browserstack_id: str = None
    browserstack_url: str = None
    public_browserstack_session_url: str = None
    command_executor: str = None
    app_center_token: str = None
    download_path: str = None
    report_portal_url: str = None
    zephyr_url: str = None
    password: str = None
    app_version: str = None
    segment: bool = None
    segment_level: str = None
    segment_token: str = None
    segment_anonymous_id: str = None
    segment_records: str = None
    headless: bool = None
    flutter: bool = None
    inactive_environment_prod: bool = None
    web_docker: bool = None
    confluence_report: bool = None
    result_path: str = None


def _load_config_file_data(config_file):
    """ Loads the json configuration file containing session and capabilities information.

    Parameters
    ----------
    config_file: str
        The config json file path (provided for developers as capabilities_template.json).

    Returns
    -------
    dict
        The configuration file content

    Raises
    ------
    FileNotFoundError
        In case the file path does not exist

    """
    try:
        with open(config_file, encoding='utf8') as f:
            config_file_data = json.load(f)
        logger.info(f'Configuration file found at "{config_file}".')
        return config_file_data
    except FileNotFoundError as e:
        raise InvalidRemoteArgumentException(
            f'The config file path "{config_file}" does not exist on the file system.') from e
    except TypeError:
        logger.debug('The config file was not provided. Proceeding without this information.')
        return None


def _remove_empty_session_args(session_args):
    """ Removes empty session arguments from the dictionary.

    Parameters
    ----------
    session_args: dict
        The session arguments.

    Returns
    -------
    NoneType

    """
    non_empty_session_items = {key: value for key, value in session_args.items() if value}
    session_args.clear()
    session_args.update(non_empty_session_items)


def _get_config_file_session_args(config_file_data):
    """ Parses the configuration file data to retrieve the session information as arguments.

    Parameters
    ----------
    config_file_data: dict
        The content of the configuration file.

    Returns
    -------
    dict
        The session valid information argument data.

    """
    session_args = config_file_data.get(_SESSION_CONFIG_FILE_KEY)
    session_args = dict(
        platform=session_args.pop(Capabilities.PLATFORM_NAME, None),
        browserstack_user=session_args.pop(SessionKeys.BROWSERSTACK_USER, None),
        browserstack_key=session_args.pop(SessionKeys.BROWSERSTACK_KEY, None),
        **session_args
    )
    _remove_empty_session_args(session_args=session_args)

    return session_args


def _get_config_file_caps(config_file_data, session_info):
    """ Parses the configuration file data to retrieve the capabilities based on the session information.

    Parameters
    ----------
    config_file_data: dict
        The content of the configuration file.
    session_info: SessionInfo
        The parsed session info for the execution.

    Returns
    -------
    dict
        The capabilities' data for the session.

    """
    caps = config_file_data.get(_CAPABILITIES_CONFIG_FILE_KEY)
    if isinstance(caps, dict):
        caps = caps.get(session_info.platform)
        if isinstance(caps, dict):
            caps = caps.get(SessionKeys.BROWSERSTACK if session_info.browserstack else SessionKeys.LOCAL)

        app = caps.get(Capabilities.APP)
        if app:
            if isinstance(app, dict):
                caps[Capabilities.APP.value] = app.get(session_info.zone)
        device = caps.get(Capabilities.DEVICE)
        if device:
            if isinstance(device, dict):
                caps[Capabilities.DEVICE.value] = device.get(session_info.zone)

        return caps
    return None


def _get_cmd_line_session_args(cmd_line_caps, **cmd_line_args):
    """ Parses the command line arguments and the capabilities to retrieve the session information as arguments.

    Parameters
    ----------
    cmd_line_caps: dict
        The content of the capabilities' data provided by command line to treat special cases (e.g. platform).
    cmd_line_args: dict
        The arguments provided by command line as kwargs.

    Returns
    -------
    dict
        The session valid information argument data.

    """
    # Treating the "platform" special case, that is a capability and also a session info
    session_args = dict(
        platform=cmd_line_caps.get(Capabilities.PLATFORM_NAME) if isinstance(cmd_line_caps, dict) else None,
        **cmd_line_args
    )
    _remove_empty_session_args(session_args=session_args)

    return session_args


def _parse_items_source(cmd_line_items, config_file_items, log_pattern):
    """ Defines the final item dictionary giving priority to command line elements and logging the decision information.

    Parameters
    ----------
    cmd_line_items: dict
        The dict item from command line.
    config_file_items: dict
        The dict item the config json file.
    log_pattern: str
        The log pattern containing format entries for "key", "source" and "value"

    Returns
    -------
    dict
        Merged items giving priority to the command line.

    """
    cmd_line_items_set = set()
    config_file_items_set = set()

    # Merging caps
    final_items = {}
    if isinstance(config_file_items, dict):
        final_items.update(config_file_items)
        config_file_items_set = set(config_file_items)
    if isinstance(cmd_line_items, dict):
        final_items.update(cmd_line_items)
        cmd_line_items_set = set(cmd_line_items)

    # Logging sources
    symmetric_diff = cmd_line_items_set.symmetric_difference(config_file_items_set)
    if symmetric_diff:
        for key in symmetric_diff:
            source = _CMD_LINE_SOURCE if key in cmd_line_items_set else _CONFIG_FILE_SOURCE
            logger.debug(log_pattern.format(key=key, source=source, value=final_items[key]))
    intersection = cmd_line_items_set.intersection(config_file_items_set)
    if intersection:
        for key in intersection:
            logger.debug(log_pattern.format(key=key, source=_CMD_LINE_SOURCE, value=final_items[key]))

    return final_items


def _get_cmd_exec(platform=None, browserstack=None, browserstack_user=None, browserstack_key=None, **_):
    """ Defines the right command executor to be used according to the environment under test

    Parameters
    ----------
    platform: str
        Check "parse_session_info" for more information.
    browserstack: bool
        Check "automation_core.remote.driver_factory" for more information.
    browserstack_user: str
        Check "automation_core.remote.driver_factory" for more information.
    browserstack_key: str
        Check "automation_core.remote.driver_factory" for more information.

    Returns
    -------
    str
        The parsed command_executor url.

    """
    cmd_exec = None
    if browserstack:
        cmd_exec = CommandExecutor.BROWSERSTACK.value.format(user=browserstack_user, key=browserstack_key)
    else:
        if platform in SUPPORTED_MOBILE_PLATFORMS:
            cmd_exec = CommandExecutor.LOCAL.value
    return cmd_exec


def _parse_session_info_source(cmd_line_session_args, config_file_session_args):
    """ Defines the final session argument values to be used on the Remote object instantiation.

    Parameters
    ----------
    cmd_line_session_args: dict
        The session info parameters retrieved from command line kwargs.
    config_file_session_args: dict
        The session info parameters retrieved from config file.

    Returns
    -------
    SessionInfo
        A named tuple with the merged session info.

    """
    final_session_info = _parse_items_source(cmd_line_items=cmd_line_session_args,
                                             config_file_items=config_file_session_args,
                                             log_pattern=_ARGUMENT_SOURCE_LOG_PATTERN)

    # Special cases
    if SessionKeys.BROWSERSTACK not in final_session_info:
        final_session_info[SessionKeys.BROWSERSTACK.value] = False
    if SessionKeys.COMMAND_EXECUTOR not in final_session_info:
        final_session_info[SessionKeys.COMMAND_EXECUTOR.value] = _get_cmd_exec(**final_session_info)

    return SessionInfo(**final_session_info)


def _add_browserstack_caps(caps, session_info):
    """ Adds new capabilities to the current capabilities' dictionary to be uploaded to the browserstack platform.

    We can add any key=value we want to the browserstack capabilities and use this keys later for many purposes.
    E.g. filtering.

    Parameters
    ----------
    caps: dict
        The capabilities' dict to have new added keys.
    session_info: SessionInfo
        A named tuple with session info data.

    Returns
    -------
    NoneType

    """
    caps[Capabilities.PROJECT.value] = session_info.project
    caps[Capabilities.BUILD.value] = BROWSERSTACK_BUILD_NAME_PATTERN.format(project=session_info.project,
                                                                            platform=session_info.platform,
                                                                            environment=session_info.environment,
                                                                            zone=session_info.zone,
                                                                            timestamp=datetime.utcnow().isoformat())
    if Capabilities.OS_VERSION in caps and not caps[Capabilities.OS_VERSION]:
        caps.pop(Capabilities.OS_VERSION)

    if session_info.platform != Platform.WEB:
        caps[Capabilities.BS_APPIUM_VERSION.value] = APPIUM_V1_22_0


def _add_flutter_caps(caps):
    """ Adds new capabilities to the current capabilities' dictionary in order to run flutter based applications.

     Parameters
    ----------
    caps: dict
        The capabilities' dict to have new added keys.

    Returns
    -------
    NoneType

    """
    caps[Capabilities.AUTOMATION_NAME.value] = _FLUTTER_AUTOMATION_NAME


def _add_headless_caps(caps):
    """ Include the --headless argument on caps if Chrome or Firefox
    parameters:
        caps: dict
            The capabilities' dict to have new added keys.
    Returns:
        NoneType
    """
    # TODO add safari
    if caps.get(Capabilities.BROWSER_NAME) == Browser.CHROME:
        _merge_driver_options_args(Capabilities.CHROME_OPTIONS.value, Capabilities.CHROME_ARGS.value,
                                   _CHROME_CAP_HEADLESS, caps)
    elif caps.get(Capabilities.BROWSER_NAME) == Browser.FIREFOX:
        _merge_driver_options_args(Capabilities.FIREFOX_OPTIONS.value, Capabilities.FIREFOX_ARGS.value,
                                   _FIREFOX_CAP_HEADLESS, caps)
    else:
        logger.error('Headless mode only supported for "Firefox" or "Chrome" browsers. Testing will continue with '
                     'headless disabled.')


def _merge_driver_options_args(driver_options, driver_args, new_capability, caps):
    """
    Include the --headless as argument on caps dict

    Args:
        driver_options: str
        driver_args: str
            The name of the kwarg key that should be changed
        new_capability: dict
            The value of kwarg that will be added as a new capability
        caps: dict
            The capabilities' dict to have new added keys.

    Returns:
        NoneType
    """
    current_driver = caps.get(driver_options)
    if current_driver:
        current_args = current_driver.get(driver_args)
        if current_args:
            current_args.extend(
                x for x in new_capability[driver_args] if x not in current_args
            )
        else:
            current_driver[driver_args] = new_capability[driver_args]
    else:
        caps[driver_options] = new_capability


def _add_firefox_local_caps(caps):
    """ Adds capabilities for running firefox locally with marionette GeckoDriver module.

    Parameters
    ----------
    caps: dict
        The capabilities' dict to have new added keys.

    Returns
    -------
    NoneType

    """
    if caps.get(Capabilities.MARIONETTE) is not False:
        caps[Capabilities.MARIONETTE.value] = True


def _parse_caps_source(cmd_line_caps, config_file_caps, session_info):
    """ Defines the final capability dictionary used to instantiate the remote object and logs details to the user.

    Parameters
    ----------
    cmd_line_caps: dict
        The capabilities from command line.
    config_file_caps: dict
        The capabilities from the config json file.
    session_info: SessionInfo
        The parsed session info for the execution.

    Returns
    -------
    dict
        Merged capabilities.

    """
    caps = _parse_items_source(cmd_line_items=cmd_line_caps,
                               config_file_items=config_file_caps,
                               log_pattern=_CAPABILITY_SOURCE_LOG_PATTERN)

    # Special cases
    if session_info.browserstack:
        _add_browserstack_caps(caps=caps, session_info=session_info)
    else:
        if session_info.platform == Platform.WEB:
            if caps.get(Capabilities.BROWSER_NAME) == Browser.FIREFOX:
                _add_firefox_local_caps(caps=caps)

    if session_info.headless:
        if session_info.platform == Platform.WEB and not session_info.browserstack:
            _add_headless_caps(caps=caps)

    if session_info.flutter:
        _add_flutter_caps(caps=caps)

    return caps


def _check_session_info_required_args(session_info):
    """ Validates required arguments for minimal Remote object instantiation.

    Parameters
    ----------
    session_info: SessionInfo
         A named tuple with session info data.

    Returns
    -------
    NoneType

    Raises
    -------
    InvalidRemoteArgumentException
        In case some required argument is invalid or missing.

    """
    if not session_info.environment:
        raise InvalidRemoteArgumentException(f'The "{SessionKeys.ENVIRONMENT}" was not provided.')
    if session_info.browserstack:
        if not session_info.browserstack_user:
            raise InvalidRemoteArgumentException(f'The "{SessionKeys.BROWSERSTACK_USER}" was not provided.')
        if not session_info.browserstack_key:
            raise InvalidRemoteArgumentException(f'The "{SessionKeys.BROWSERSTACK_KEY}" was not provided.')
    if session_info.headless:
        if session_info.browserstack:
            logger.error('Headless NOT supported on BrowserStack executions. Testing will continue with '
                         'headless disabled.')
            session_info.headless = False
        if session_info.platform != Platform.WEB:
            logger.error(f'Headless NOT supported for platform "{session_info.platform}". Testing will continue with '
                         f'headless disabled.')
            session_info.headless = False


def get_execution_data(config_file, cmd_line_caps, **cmd_line_args):
    """ Get the required data to instantiate the Remote object parsing data from the command line and  the config file.

    Parameters
    ----------
    config_file: str
        The config json file path (provided for developers as capabilities_template.json).
    cmd_line_caps: dict
        The content of the capabilities' data provided by command line to treat special cases (e.g. platform).
    cmd_line_args: kwargs
        The arguments provided by command line.

    Returns
    -------
    SessionInfo
        A named tuple with the merged session info.
    dict
        Merged capabilities.

    """
    cmd_line_session_args = _get_cmd_line_session_args(cmd_line_caps=cmd_line_caps, **cmd_line_args)
    config_file_data = _load_config_file_data(config_file=config_file)
    config_file_session_args = None

    if config_file_data:
        config_file_session_args = _get_config_file_session_args(config_file_data=config_file_data)

    session_info = _parse_session_info_source(cmd_line_session_args=cmd_line_session_args,
                                              config_file_session_args=config_file_session_args)
    _check_session_info_required_args(session_info=session_info)
    config_file_caps = None

    if config_file_data:
        config_file_caps = _get_config_file_caps(config_file_data=config_file_data, session_info=session_info)

    caps = _parse_caps_source(cmd_line_caps=cmd_line_caps, config_file_caps=config_file_caps, session_info=session_info)

    return session_info, caps
