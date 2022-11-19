from appium.webdriver.common.appiumby import AppiumBy

from project.config import mapping


@mapping(page='login')
class LoginMapping:
    TXT_USER = (AppiumBy.XPATH, "//android.widget.EditText[contains(@resource-id,'sername')] "
                                "| //*[@resource-id='signInName']")

    TXT_PASSWORD = (AppiumBy.XPATH, "//android.widget.EditText[contains(@resource-id,'assword')] "
                                    "| //*[@resource-id='password']")
    BTN_SUBMIT = (AppiumBy.XPATH, "//android.widget.Button[contains(@resource-id,'login')] "
                                  "| //*[@resource-id='newSubmitBtn']")
    TXT_PASSWORD_ALERT_MSG = (AppiumBy.XPATH, "//*[@resource-id='errorBlockpassword']/"
                                              "android.widget.TextView[not(contains(@text,''))]")
    TXT_USER_ALERT_MSG = (AppiumBy.XPATH, "//*[@resource-id='errorBlocksignInName']/"
                                          "android.widget.TextView[not(contains(@text,''))]")
    TXT_TIP_MSG = (AppiumBy.XPATH, "(//*[@resource-id='errorBlocksignInName']//android.widget.TextView)[2]")
