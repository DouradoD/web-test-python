from selenium.webdriver import Remote, Chrome, Edge, Firefox, Safari
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from .page_factory import Pages
from .session_info import get_execution_data
from .constants import Capabilities
from .utils.utils import caps_to_options


class Browser:
    """ Browser names """

    CHROME = 'chrome'
    EDGE = 'edge'
    FIREFOX = 'firefox'
    SAFARI = 'safari'


# Map to store the correct driver class, driver manager and driver service for each browser
_LOCAL_BROWSER_DRIVER_MAP = {
    Browser.CHROME: (Chrome, ChromeDriverManager, ChromeService),
    Browser.EDGE: (Edge, EdgeChromiumDriverManager, EdgeService),
    Browser.FIREFOX: (Firefox, GeckoDriverManager, FirefoxService),
    Browser.SAFARI: (Safari, None, SafariService)  # TODO: As Safari is not supported by "webdriver_manager" lib,
    # the executor must be
    #  manually installed
}


class BrowserNotSupportedForLocalRunException(Exception):
    """ The browser is not supported for local test running.

    """


def web_driver_cls_factory(browser_name, browserstack, web_docker=None):
    """ Gets the proper WebRemote class according to the inputs

    Parameters
    ----------
    browser_name: Enum/str
        The browser name under test.
    web_docker: bool
        Indicates that the remote object is set to be run on the docker using the selenium standalone defined on
         docker compose file when the browserstack parameter is false or None

    Returns
    -------
    type
        The WebRemote class to be used on the final driver

    Raises
    ------
    BrowserNotSupportedForLocalRunException
        In case The browser is invalid or not provided.

    """

    driver_manager = None
    if browserstack:
        base_cls = Remote
    elif web_docker:
        base_cls = Remote
    else:
        try:
            base_cls, driver_manager, driver_service = _LOCAL_BROWSER_DRIVER_MAP[browser_name]
        except KeyError:
            raise BrowserNotSupportedForLocalRunException(
                f'The browser "{browser_name if browser_name else "empty"}" '
                f'is not supported for local runs.') from KeyError

    class CustomRemote(base_cls):
        def __init__(self, desired_capabilities=None, command_executor=None, **other_params):
            """ Constructor

            Parameters
            ----------
            desired_capabilities: dict
                The capabilities as it is passed on Selenium.
            command_executor: str
                A string representing URL of the remote server.
            other_params: dict
                Another params to start the service and create new instance of driver as kwargs.

            Returns:
                Custom selenium driver
            """
            desired_capabilities.pop(Capabilities.PLATFORM_NAME, None)
            options = caps_to_options(browser_name, desired_capabilities)
            params = dict(options=options, **other_params)
            if web_docker and not command_executor:
                # This command executor is used to run the tests using the selinium hub!
                # To do it, we need to pass the executor using the following structure:
                # http://<CONTAINER_SELENIUM_HUB_NAME>:4444/wd/hub
                params.update(dict(command_executor='http://selenium-hub:4444/wd/hub'))
            elif command_executor:
                params.update(dict(command_executor=command_executor))
            if driver_manager:
                params.update(dict(service=driver_service(driver_manager().install())))
            super().__init__(**params)

    return CustomRemote


def driver_factory(desired_capabilities=None,
                   command_executor=None,
                   config_file=None,
                   session_info=None,
                   web_docker=False,
                   environment=None,
                   browserstack=None,
                   browserstack_user=None,
                   browserstack_key=None,
                   **other_params):
    if not (session_info and desired_capabilities):
        session_info, desired_capabilities = get_execution_data(config_file=config_file,
                                                                cmd_line_caps=desired_capabilities,
                                                                command_executor=command_executor,
                                                                environment=environment,
                                                                browserstack=browserstack,
                                                                browserstack_user=browserstack_user,
                                                                browserstack_key=browserstack_key,
                                                                web_docker=web_docker)

    class RemoteDriver(web_driver_cls_factory(browser_name=desired_capabilities.get('browserName'),
                                              browserstack=session_info.browserstack)):

        def __init__(self):
            self._desired_capabilities = desired_capabilities
            self._command_executor = session_info.command_executor
            self._other_params = other_params
            super().__init__(desired_capabilities=self._desired_capabilities,
                             command_executor=self._command_executor,
                             **self._other_params)
            self._pages = Pages(driver=self)

        @property
        def pages(self):
            """ The mapped pages for the given requirements.

            Returns
            -------
            Pages
                The automation pages object.

            """
            return self._pages

    return RemoteDriver()
