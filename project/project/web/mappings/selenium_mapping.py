from selenium.webdriver.common.by import By
from project.config import mapping


@mapping(page='selenium_home')
class SeleniumMapping:
    LOGO = (By.ID, 'selenium_logo')
