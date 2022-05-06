from .selenium_home import SeleniumHome


class Pages:
    @staticmethod
    def selenium_home(driver):
        return SeleniumHome(driver)
