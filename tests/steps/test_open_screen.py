from pytest_bdd import scenarios, when, then, parsers
from tests.pages.selenium_actions import Selenium

scenarios('../features/open_screen.feature')


@when(parsers.parse('the user accesses the following url "{url}"'))
def impl(driver, url):
    driver.get(url)


@then('the Selenium io screen should be visible')
def impl(driver):
    Selenium(driver=driver).is_on_focus()
