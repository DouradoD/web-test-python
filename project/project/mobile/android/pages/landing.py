from project.config import page


@page(name='landing')
class Landing:

    def sign_in(self):
        self.driver.actions.wait_until_element_clickable(self.mapping.BTN_SIGN_IN).click()
