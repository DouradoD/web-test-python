from project.config.utils.utils import LoadCmdLineCapabilities
from project.config.plugins.hooks import Hooks


def pytest_addoption(parser):
    """ Pytest initialization hook """

    group = parser.getgroup('Gold Automation')
    group.addoption(
        '--capabilities', nargs='*', action=LoadCmdLineCapabilities,
        help='The environment capabilities necessary to run the test(provide as '
             'a whitespace separated list of key=value pairs (Surround the value by double quotes in case the value '
             'itself contains whitespaces).',
    )
    group.addoption(
        '--cmd-exec', help='The Appium remote server address.', default=None
    )
    group.addoption(
        '--environment', help='The environment under testing.', default=None,
    )
    group.addoption(
        '--web-docker', action='store_true', help='Run test using the chrome selenium standalone image '
                                                  'from docker if browserstack parameter is false/None'
    )
    group.addoption(
        '--browserstack', action='store_true', help='Run project by using browserstack platform.'
    )
    group.addoption(
        '--browserstack-user', default=None, help='The browserstack username for login.',
    )
    group.addoption(
        '--browserstack-key', default=None, help='The browserstack API key for login.',
    )
    group.addoption(
        '--app-center-token', default=None, help='The App Center API token for app download.',
    )
    group.addoption(
        '--headless', action='store_true', help='Enables execution in web headless state.'
    )
    group.addoption(
        '--config-file', default=None,
        help='The path to a json configuration file (Including session and capabilities info). '
             'it is an additional option for providing the necessary input arguments for running '
             'the project.',
    )


def pytest_configure(config):
    """ Pytest initialization hook """

    # Ignoring mark warnings as we are using marks to filter the project and there is no need to track them all
    config.addinivalue_line(
        'filterwarnings', 'ignore::pytest.PytestUnknownMarkWarning'
    )
    config.pluginmanager.register(Hooks(config=config), 'hooks')
