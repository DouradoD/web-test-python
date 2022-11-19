from project.config import page
from project.config.logger import logger
from hamcrest import assert_that, contains_string


@page(name='login')
class LoginSIT:

    def fill_the_user_field(self, username):
        self.driver.actions.wait_until_element_clickable(self.mapping.TXT_USER).send_keys(username)

    def fill_the_password_field(self, password):
        self.driver.actions.wait_until_element_clickable(self.mapping.TXT_PASSWORD).send_keys(password)

    def submit(self):
        self.driver.actions.wait_until_element_clickable(self.mapping.BTN_SUBMIT).click()

    def check_the_login_error_message(self, user_type, password_type):

        user_types = (
            'invalid-user', 'registered-email', 'registered-phone', 'not-registered-email', 'empty-input',
            'not-registered-phone')
        password_types = ('invalid-password', 'valid-password', 'empty-input')

        if user_type not in user_types:
            raise ValueError(
                f'The "user_type" parameter must be one of the following: {", ".join(user_types)}')
        if password_type not in password_types:
            raise ValueError(
                f'The "password_type" parameter must be one of the following: {", ".join(password_types)}')

        if password_type == 'empty-input':
            logger.info('Checking logging error message for password field...')
            self.driver.actions.wait_until_element_visible(self.mapping.TXT_PASSWORD_ALERT_MSG)
            shown_password_alert_msg = self.driver.actions.wait_until_element_visible(
                self.mapping.TXT_PASSWORD_ALERT_MSG).text.strip()
            expected_password_alert_msg = self.driver.data.messages['messages']['login']['empty-password']
            logger.info(f'\tExpected password alert message: {expected_password_alert_msg}')
            logger.info(f'\tActual password alert message: {shown_password_alert_msg}')
            assert_that(shown_password_alert_msg, contains_string(expected_password_alert_msg))

        if not (user_type in ['registered-email', 'registered-phone'] and password_type == 'empty-input'):
            logger.info('Checking logging error message for user field...')
            shown_user_alert_msg = self.driver.actions.wait_until_element_visible(
                self.mapping.TXT_USER_ALERT_MSG).text.strip()
            error_msg_key_query = (user_type if user_type in (
                'invalid-user', 'not-registered-email', 'not-registered-phone', 'empty-input') else password_type)
            expected_user_alert_msg = self.driver.data.messages['messages']['login'][error_msg_key_query]
            logger.info(f'\tExpected password alert message: {expected_user_alert_msg}')
            logger.info(f'\tActual password alert message: {shown_user_alert_msg}')
            assert_that(shown_user_alert_msg, contains_string(expected_user_alert_msg))
