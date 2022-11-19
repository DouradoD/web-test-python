from pytest_bdd import scenarios, when, then, parsers, given
from hamcrest import assert_that, contains_string

scenarios('../features/login.feature')


@given('that Marcos as an ADM user is in the login screen')
def impl(driver):
    driver.pages.landing.sign_in()


@given(parsers.parse('he fills the user field with the following "{user}" value'))
def impl(driver, user):
    driver.pages.login.fill_the_user_field(user)


@given(parsers.parse('he fills the pass field with the following "{password}" value'))
def impl(driver, password):
    driver.pages.login.fill_the_password_field(password)


@when('he triggers the login option')
def impl(driver):
    driver.pages.login.submit()


@then('the message about invalid value should be displayed')
def impl(driver):
    driver.actions.wait_until_element_visible(driver.pages.login.mapping.TXT_USER_ALERT_MSG)
    shown_password_alert_msg = driver.actions.wait_until_element_visible(
        driver.pages.login.mapping.TXT_USER_ALERT_MSG).text.strip()
    expected_password_alert_msg = 'Insira um número de celular ou e-mail válido.'
    assert_that(shown_password_alert_msg, contains_string(expected_password_alert_msg))
