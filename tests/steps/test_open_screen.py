from pytest_bdd import scenarios, when, then, parsers
from tests.pages.page_factory import Pages

scenarios('../features/open_screen.feature')


@when(parsers.parse('the user accesses the following url "{url}"'))
def impl(driver, url):
    driver.get(url)


@then('the Selenium screen should be visible')
def impl(driver):
    Pages.selenium_home(driver).is_on_focus()
