'''
list command
'''

import logging
import os

import dockerapp

def init_parser(parser):
    pass

def run(args, unknown_args):
    logging.info(' '.join(os.listdir(dockerapp.PATH_APPS)))

