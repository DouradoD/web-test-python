from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class ElementsTextNotMatchException(Exception):
    """ Exception raised when elements texts do not match within a given timeout. """


class CommonActions:
    _TIME_STEP = .5  # Default time step for timeout handling (polling)
    _TIMEOUT_ERROR_MESSAGE = ('The condition "{condition}" was not match for the element(s) located by "{by}" within '
                              '{timeout} seconds.')

    CUSTOM_IGNORED_EXCEPTIONS = (StaleElementReferenceException,)

    # Timeouts
    TINY_TIMEOUT = 5
    SHORT_TIMEOUT = 15
    LONG_TIMEOUT = 25

    def __init__(self, driver):
        self._driver = driver

    def check_condition(self, by, condition):
        """ Check if an element provided by the given parameters matches a condition.

        Parameters
        ----------
        by: tuple
            The locator strategy given by the method and the value.
        condition: callable
            The callable object that represents a condition. Usually retrieved from the module
            "selenium.webdriver.support.expected_conditions".

        Returns
        -------
        bool
            True if the condition is satisfied, False otherwise.

        """
        check_condition = condition(by)

        try:
            return bool(check_condition(self._driver))
        except (NoSuchElementException,) + self.CUSTOM_IGNORED_EXCEPTIONS:
            return False

    def wait_until_element_condition(self, by, condition, timeout=None, ignored_exceptions=None,
                                     custom_message_exception=''):
        """ Wait for an element located by the given search parameters to match the condition.

        Parameters
        ----------
        by: tuple
            The locator strategy given by the method and the value.
        condition: callable
            The callable object that represents a condition. Usually retrieved from the module
            "selenium.webdriver.support.expected_conditions".
        timeout: int
            The timeout in seconds. By default, it waits for the timeout defined by the class constant "SHORT_TIMEOUT".
        ignored_exceptions: tuple
            The exceptions that should be ignored by the web driver. By default, it ignores the exceptions listed on the
            class constant "CUSTOM_IGNORED_EXCEPTIONS".
        custom_message_exception: str
            Custom Message Exception Add-on.

        Returns
        -------
        bool
            Returns the result of the condition method, if there is no exception

        Raises
        ------
        TimeoutException
            Raised if the condition is not satisfied within the given timeout.

        """
        # Loading defaults
        ignored_exceptions = ignored_exceptions or self.CUSTOM_IGNORED_EXCEPTIONS
        timeout = timeout or self.SHORT_TIMEOUT

        # Instantiating the wait object
        web_driver_wait = WebDriverWait(driver=self._driver, timeout=timeout, ignored_exceptions=ignored_exceptions)

        # Defining an error message
        message = self._TIMEOUT_ERROR_MESSAGE.format(
            condition=condition.__name__,
            by=by,
            timeout=timeout)
        if custom_message_exception:
            message = message + f'\n Custom message: {custom_message_exception}'

        return web_driver_wait.until(method=condition(by), message=message)

    def wait_until_element_visible(self, by, timeout=None, ignored_exceptions=None, custom_message_exception=''):
        """ Wait until an element is visible.

        Parameters
        ----------
        by: tuple
            The locator strategy.
        timeout: int
            The timeout in seconds.
        ignored_exceptions: tuple
            The exceptions that should be ignored by the web driver.
        custom_message_exception: str
            Custom Message Exception Add-on.

        Raises
        ------
        TimeoutException
            Raised if the condition is not satisfied within the given timeout.

        """
        return self.wait_until_element_condition(by=by, timeout=timeout, ignored_exceptions=ignored_exceptions,
                                                 condition=expected_conditions.visibility_of_element_located,
                                                 custom_message_exception=custom_message_exception)

    def wait_until_element_clickable(self, by, timeout=None, ignored_exceptions=None, custom_message_exception=''):
        """ Wait until an element is clickable.

        Parameters
        ----------
        by: tuple
            The locator strategy.
        timeout: int
            The timeout in seconds.
        ignored_exceptions: tuple
            The exceptions that should be ignored by the web driver.
        custom_message_exception: str
            Custom Message Exception Add-on.

        Raises
        ------
        TimeoutException
            Raised if the condition is not satisfied within the given timeout.

        """
        return self.wait_until_element_condition(by=by, timeout=timeout, ignored_exceptions=ignored_exceptions,
                                                 condition=expected_conditions.element_to_be_clickable,
                                                 custom_message_exception=custom_message_exception)

    def wait_until_element_selected(self, by, timeout=None, ignored_exceptions=None, custom_message_exception=''):
        """ Wait until an element is selected.

        Parameters
        ----------
        by: tuple
            The locator strategy.
        timeout: int
            The timeout in seconds.
        ignored_exceptions: tuple
            The exceptions that should be ignored by the web driver.
        custom_message_exception: str
            Custom Message Exception Add-on.

        Raises
        ------
        TimeoutException
            Raised if the condition is not satisfied within the given timeout.

        """
        return self.wait_until_element_condition(by=by, timeout=timeout, ignored_exceptions=ignored_exceptions,
                                                 condition=expected_conditions.element_located_to_be_selected,
                                                 custom_message_exception=custom_message_exception)
