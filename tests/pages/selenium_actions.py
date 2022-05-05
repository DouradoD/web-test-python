from tests.mappings.selenium_mapping import SeleniumMapping


class Selenium:
    def __init__(self, driver):
        self.driver = driver
        self.selenium_mapping = SeleniumMapping()

    def is_on_focus(self):
        assert self.driver.find_element(*self.selenium_mapping.LOGO).is_displayed()
