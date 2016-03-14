'''
This module provides logging functionality:
'''

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

from __future__ import absolute_import

import logging
import sys


#------------------------------------------------------------------------------
# Formatters
#------------------------------------------------------------------------------

class ConsoleFormatter(logging.Formatter):
    FORMAT = {
            logging.DEBUG: '[DEBUG %(module)s %(lineno)d] %(msg)s',
            logging.WARN:  'Warning: %(msg)s',
            logging.ERROR: 'Exception: %(msg)s',
            logging.INFO:  '%(msg)s'
    }

    DEBUG_FORMAT = {
            logging.DEBUG: '[D %(module)s %(lineno)d] %(msg)s',
            logging.WARN:  '[W %(module)s %(lineno)d] Warning: %(msg)s',
            logging.ERROR: '[E %(module)s %(lineno)d] Exception: %(msg)s',
            logging.INFO:  '[I %(module)s %(lineno)d] %(msg)s'
    }

    def __init__(self):
        super(ConsoleFormatter, self).__init__()
        self.verbose = False


    def format(self, record):
        table = {True: self.DEBUG_FORMAT, False: self.FORMAT}.get(self.verbose)
        self._fmt = table.get(record.levelno, self.FORMAT[logging.INFO])
        return logging.Formatter.format(self, record)


#------------------------------------------------------------------------------
# Helper functions
#------------------------------------------------------------------------------

def add_console_handler(logger):
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(ConsoleFormatter())
    logger.addHandler(stdout_handler)

def init(quiet=False, verbose=False):
    logger = logging.getLogger()

    # Slightly dodgy - we are assigning to a member variable
    # since there is no logging.Logger method for clearing the list
    # of handlers
    logger.handlers = []

    add_console_handler(logger)

    if not quiet:
        logger.setLevel(logging.INFO)

    if verbose:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            formatter = handler.formatter
            formatter.verbose = True

