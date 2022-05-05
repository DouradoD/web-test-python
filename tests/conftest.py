import pytest
import selenium.webdriver
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from pytest_bdd import given, then, parsers


@pytest.fixture(scope='session')
def driver():
    opts = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    return driver


def pytest_bdd_before_scenario(request, feature, scenario):
    driver = request.getfixturevalue('driver')
    driver.maximize_window()

# def pytest_bdd_after_scenario():
#     # Quit the WebDriver instance for the teardown
#     driver.quit()
