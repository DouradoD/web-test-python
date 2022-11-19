from appium.webdriver.common.appiumby import AppiumBy
from project.config import mapping


@mapping(page='landing')
class LandingMapping:
    IV_REBRANDING_LOGO = (AppiumBy.XPATH, '//*[contains(@resource-id, "logoImageView")]')
    BTN_SIGN_IN = (AppiumBy.XPATH, '//*[contains(@resource-id, "signinButton")]')
    BTN_SIGN_UP = (AppiumBy.XPATH, '//*[contains(@resource-id, "signupButton")]')
