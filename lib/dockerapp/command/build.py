'''
build command
'''

import logging
import os

import dockerapp
from dockerapp import app
from dockerapp import docker

def init_parser(parser):
    parser.add_argument(
        'name',
        metavar = 'NAME',
        help = 'application name')

def run(args, unknown_args):
    logging.info('Building {:s}'.format(args.name))
    config = app.Config(args.name)
    docker.build(config)

