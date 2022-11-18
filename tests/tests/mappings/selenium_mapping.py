from selenium.webdriver.common.by import By
from tests.config import mapping


@mapping(name='selenium_home')
class SeleniumMapping:
    LOGO = (By.ID, 'selenium_logo')
