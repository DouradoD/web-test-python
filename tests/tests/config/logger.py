""" The customized logger for automation.

Examples
--------
Normal usage:

>>> from tests.config import logger
>>> logger.info('Info message')
INFO: Info message
>>> logger.warning('Warning message')
WARNING: Warning message

Setting the level:
>>> logger.setLevel(level=logging.DEBUG)  # Setting the logger to print debug logs

See Also
--------
Check the logging official page to get the supported levels and features:
https://docs.python.org/3/library/logging.html

"""
import logging

# create logger with 'spam_application'
logger = logging.getLogger()
# setting logger level
logger.setLevel('NOTSET')

LINE_SEPARATION_LENGTH = 80
LINE_SEPARATION = '=' * LINE_SEPARATION_LENGTH
