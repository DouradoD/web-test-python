import pytest
from project.config.session_info import get_execution_data
from project.config.remote import driver_factory


class Hooks:
    def __init__(self, config):
        self._config = config
        self._capabilities = self._config.getoption('--capabilities')
        self._command_executor = self._config.getoption('--cmd-exec')
        self._environment = self._config.getoption('--environment')
        self._run_on_bs = self._config.getoption('--browserstack')
        self._bs_user = self._config.getoption('--browserstack-user')
        self._bs_key = self._config.getoption('--browserstack-key')
        self._config_file_path = self._config.getoption('--config-file')
        self._headless = self._config.getoption('--headless')
        self._web_docker = self._config.getoption('--web-docker')
        # Execution variables
        self._session_info = None
        self._desired_capabilities = None
        self._driver = None

    @pytest.fixture(scope='session')
    def driver(self):
        """ Fixture to provide the automation_core.Remote object all set for running the project. """

        # Setup for the driver object
        ...

        yield self._driver

        # Tear down for the driver object
        ...

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, items):
        """
            Called after collection has been performed. May filter or re-order the items in-place.
        Args:
            items:List[pytest.Item]
                List of item objects.
        """

        if items:
            self._session_info, self._desired_capabilities = get_execution_data(
                config_file=self._config_file_path,
                cmd_line_caps=self._capabilities,
                command_executor=self._command_executor,
                environment=self._environment,
                browserstack=self._run_on_bs,
                browserstack_user=self._bs_user,
                browserstack_key=self._bs_key,
                headless=self._headless,
                web_docker=self._web_docker
            )

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self):
        """
            Pytest run test hook: Called to perform the setup phase for a test item.
            The default implementation runs setup() on item and all of its parents (which haven’t been setup yet).
            This includes obtaining the values of fixtures required by the item (which haven’t been obtained yet).
        Args:
            item: Function
                All information about the execution

        """

        if not self._driver:
            self._driver = driver_factory(desired_capabilities=self._desired_capabilities,
                                          session_info=self._session_info)
