'''
Docker interface.
'''

import logging
import os
import subprocess

import dockerapp
from dockerapp import util

CAPABILITY = {
    'audio': {
        'device': {
            '/dev/snd': {}
        },
    },

    'display': {
        'environment': {
            'DISPLAY': 'unix${DISPLAY}',
        },
        'volume': {
            '/tmp/.X11-unix': {},
        },
    },
}


def image_version(name):
    return 'latest'


class Run(object):
    '''
    Helper class for building 'docker run' arguments.
    '''
    def __init__(self, config, args, env, tty):
        name = config['name']

        self.args = [ 'docker', 'run' ]
        self.args += [ '--name', name ]

        if tty:
            self.args.append('--tty')

        for c in config.get('capability', []):
            cap = CAPABILITY[c]
            util.tree_subst_env(cap)
            self.update(cap)

        self.update(config)

        version = image_version(name)
        self.args += [ '{:s}:{:s}'.format(name, version) ]

        self.args += args

    def update(self, config):
        self.add_devices(config.get('device', {}))
        self.add_env_vars(config.get('environment', {}))
        self.add_volumes(config.get('volume', {}))

    def add_devices(self, devices):
        for path_container, data in devices.iteritems():
            path_host = data.get('host', path_container)
            dev = '{:s}:{:s}'.format(path_host, path_container)
            self.args +=  [ '--device', dev ]

    def add_env_vars(self, env):
        for k, v in env.iteritems():
            self.args += [ '-e', '{:s}={:s}'.format(k, str(v)) ]

    def add_volumes(self, volumes):
        for path_container, data in volumes.iteritems():
            path_host = data.get('host', path_container)
            vol = '{:s}:{:s}'.format(path_host, path_container)
            if data.get('readonly', False):
                vol += ':ro'
            self.args += [ '--volume', vol ]


def run(config, args, env=None, tty=False):
    '''
    Run application described in config, with arguments args.
    '''
    r = Run(config, args, env=env, tty=tty)

    logging.info(' '.join(r.args))

    subprocess.call(r.args)


def build(config):
    name = config['name']

    # TODO: add a flag to app.yaml which declares whether the app needs to be
    # run under a particular UID
    uid = os.getuid()

    args = [ 'docker', 'build' ]

    if uid is not None:
        args += [ '--build-arg', 'DOCKERAPP_UID={:s}'.format(str(uid)) ]

    version = image_version(name)
    args += [ '-t', '{:s}:{:s}'.format(name, version) ]

    args.append(os.path.join(dockerapp.PATH_APPS, name))

    logging.info(' '.join(args))

    subprocess.call(args)

