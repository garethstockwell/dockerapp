'''
run command
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

    parser.add_argument(
        '--tty',
        dest = 'tty',
        action = 'store_true',
        default = False)

def run(args, unknown_args):
    logging.info('Running {:s} (arguments [{:s}])'.format(
        args.name, ' '.join(unknown_args)))
    config = app.Config(args.name)
    docker.run(config, unknown_args, tty=args.tty)

