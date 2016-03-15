'''
run command
'''

import logging
import os

import dockerapp
from dockerapp import app
from dockerapp import docker
from dockerapp import util

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

    parser.add_argument(
        '--detach',
        dest = 'detach',
        choices = ('yes', 'no'),
        help = 'run detached from TTY')

    parser.add_argument(
        '--shell',
        dest = 'shell',
        action = 'store_true',
        default = False)


def run(args, unknown_args):
    config = app.Config(args.name)

    if args.detach is not None:
        config['option.detach'] = util.str_to_bool(args.detach)

    if docker.is_running(args.name):
        docker.restart(args.name)
    else:
        docker.run(config, unknown_args, tty=args.tty, shell=args.shell)

