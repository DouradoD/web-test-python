from enum import Enum, EnumMeta


# Groups
class EnvironmentEnumMeta(EnumMeta):
    """
    Class to implement changes on EnumMeta to better support structured constants

        cls VS self
            Function and method arguments:
                Always use self for the first argument to instance methods.
                Always use cls for the first argument to class methods.
    """

    def __contains__(cls, item):
        """
        Python string __contains__() is an instance method and returns boolean value True or False
        depending on whether the string object contains the specified string object or not.
        Args:
            item: str
                The item string object to be compared
        Returns: bool
        """
        try:
            #  Enums do not comply to conventional constructor rules
            cls(item)  # pylint: disable=no-value-for-parameter
            return True
        except ValueError:
            return False


class EnvironmentEnum(Enum, metaclass=EnvironmentEnumMeta):
    """ Class to handle structured constants """

    def __eq__(self, other):
        """
        Python __eq__ method to compare two objects by their values.
        Args:
            other: str
                The item to be compared
        Returns: bool

        """
        if isinstance(other, EnvironmentEnum):
            return self is other
        if isinstance(other, str):
            return self.value == other
        return False

    def __hash__(self):
        """" The hash() function accepts an object and returns the hash value as an integer.
        When you pass an object to the hash() function, Python will execute the __hash__ special method of the object.
        By default, the __hash__ uses the object's identity and the __eq__ returns True if two objects are the same. """
        return hash(self.value)

    def __str__(self):
        """ The __str__ method in Python represents the class objects as a string – it can be used for classes.
        The __str__ method should be defined in a way that is easy to read and outputs all the members of the class.
        This method is also used as a debugging tool when the members of a class need to be checked. """
        return self.value

    @classmethod
    def get_members(cls):
        """
        Returns: list
            list of each item.value contained on self/cls!
        """
        return [item.value for item in cls]


class Capabilities(EnvironmentEnum):
    """ Capabilities keys mapping """

    PLATFORM_NAME = 'platformName'
    BROWSER_NAME = 'browserName'
    APP = 'app'
    DEVICE_NAME = 'deviceName'
    OS_VERSION = 'os_version'
    # For BrowserStack only
    DEVICE = 'device'
    MOBILE = 'mobile'
    PROJECT = 'project'
    BUILD = 'build'
    NAME = 'name'
    BROWSER = 'browser'
    # For app download
    APP_VERSION = 'app_version'
    APP_VERSION_ID = 'app_version_id'
    APP_FORCE_DOWNLOAD = 'app_force_download'

    # For running headless tests
    CHROME_OPTIONS = 'goog:chromeOptions'
    CHROME_ARGS = 'args'
    FIREFOX_OPTIONS = 'moz:firefoxOptions'
    FIREFOX_ARGS = 'args'

    # For firefox local execution
    MARIONETTE = 'marionette'

    # For flutter based apps
    AUTOMATION_NAME = 'automationName'

    # To force browserstack appium on specific version
    BS_APPIUM_VERSION = 'browserstack.appium_version'

    # Confluence Report
    CONFLUENCE_REPORT = 'confluence_report'
    RESULT_PATH = 'result_path'


class Platform(EnvironmentEnum):
    """ Platform types mapping """

    MOBILE = 'mobile'
    ANDROID = 'android'
    IOS = 'ios'
    WEB = 'web'
    FLUTTER = 'flutter'


class Browser(EnvironmentEnum):
    """ Browser names """

    CHROME = 'chrome'
    EDGE = 'edge'
    FIREFOX = 'firefox'
    SAFARI = 'safari'


class Environment(EnvironmentEnum):
    """ Environment """

    UAT = 'uat'
    SIT = 'sit'
    PROD = 'prod'
    QA = 'qa'
    DEV = 'dev'


class Zone(EnvironmentEnum):
    """The country zones"""

    AR = 'ar'
    BO = 'bo'
    BR = 'br'
    CA = 'ca'
    CL = 'cl'
    CO = 'co'
    DO = 'do'
    EC = 'ec'
    GB = 'gb'
    HN = 'hn'
    MX = 'mx'
    PA = 'pa'
    PE = 'pe'
    PY = 'py'
    SV = 'SV'
    TZ = 'tz'
    US = 'us'
    UY = 'uy'
    ZA = 'za'


class CommandExecutor(EnvironmentEnum):
    """ Command executor urls """

    LOCAL = 'http://127.0.0.1:4723/wd/hub'  # Appium remote server default URL
    BROWSERSTACK = 'http://{user}:{key}@hub.browserstack.com/wd/hub'


class SessionKeys(EnvironmentEnum):
    """Holds the general session constant keys other than capabilities"""

    PROJECT = 'project'
    ENVIRONMENT = 'environment'
    ZONE = 'zone'
    LOCAL = 'local'
    BROWSERSTACK = 'browserstack'
    BROWSERSTACK_USER = 'browserstack.user'
    BROWSERSTACK_KEY = 'browserstack.key'
    COMMAND_EXECUTOR = 'command_executor'
    APP_CENTER_TOKEN = 'app_center_token'
    DOWNLOAD_PATH = 'download_path'
    SEGMENT = 'segment'
    SEGMENT_LEVEL = 'segment_level'
    SEGMENT_TOKEN = 'segment_token'


class FlutterBy(EnvironmentEnum):
    """Holds the Flutter location strategies"""

    TEXT = 'text'
    TOOLTIP = 'tooltip'
    ANCESTOR = 'ancestor'
    DESCENDANT = 'descendant'
    SEMANTICS_LABEL = 'semantics_label'
    TYPE = 'type'
    VALUE_KEY = 'value_key'


# Others constants
SUPPORTED_MOBILE_PLATFORMS = [Platform.ANDROID, Platform.IOS]

RESOURCES_DIR_NAME = 'resources'

STATIC_DATA_DIR_NAME = 'static_data'

STATIC_DATA_JSON = 'data.json'

STATIC_DATA_PATH_PATTERN = f'{RESOURCES_DIR_NAME}/{STATIC_DATA_DIR_NAME}/<platform>/<zone>/YOUR_JSON_FILE(S).json'

APP_NAMES_JSON = 'app_names.json'

APP_NAMES_PATH_PATTERN = f'{RESOURCES_DIR_NAME}/{APP_NAMES_JSON}'

WEB_NAMES_JSON = 'web_version_endpoints.json'

WEB_NAMES_PATH_PATTERN = f'{RESOURCES_DIR_NAME}/{WEB_NAMES_JSON}'

PROJECT_ENTRY_POINT_TAG = 'project'

BROWSERSTACK_BUILD_NAME_PATTERN = ('{project}_'
                                   '{platform}_'
                                   '{environment}_'
                                   '{zone}_'
                                   '{timestamp}')
REPORTS_PATH = 'reports/'

UNKNOWN_VERSION = 'unknown'

APPIUM_V1_22_0 = '1.22.0'

CONFLUENCE_URL = 'https://ab-inbev.atlassian.net/wiki'
