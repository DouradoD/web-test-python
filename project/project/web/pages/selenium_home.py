from project.config import page


@page(name='selenium_home')
class SeleniumHome:

    def is_on_focus(self):
        assert self.driver.find_element(*self.mapping.LOGO).is_displayed()
