import pytest
from tests.config.remote import driver_factory as remote


@pytest.fixture(scope='session')
def driver():
    desired_capabilities = {'browser': 'chrome'}
    driver = remote(desired_capabilities=desired_capabilities)
    return driver


def pytest_bdd_before_scenario(request):
    driver = request.getfixturevalue('driver')
    driver.maximize_window()


def pytest_bdd_after_scenario(request):
    # Quit the WebDriver instance for the teardown
    driver = request.getfixturevalue('driver')
    driver.quit()
