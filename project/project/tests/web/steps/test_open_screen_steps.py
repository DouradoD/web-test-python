from pytest_bdd import scenarios, when, then, parsers

scenarios('../features/open_screen.feature')


@when(parsers.parse('the user accesses the following url "{url}"'))
def impl(driver, url):
    driver.get(url)


@then('the Selenium screen should be visible')
def impl(driver):
    driver.pages.selenium_home.is_on_focus()
