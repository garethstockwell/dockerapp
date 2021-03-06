'''
Docker interface.
'''

import logging
import os
import subprocess

import dockerapp
from dockerapp import util

AUDIO_SND = {
    'device': {
        '/dev/snd': {}
    },
}

AUDIO_PULSE_USER_V1 = {
    'volume': {
        '/dev/shm': {},
        '/home/user/.pulse': {
            'host': '${HOME}/.pulse',
        },
        '/run/user/${USER_UID}/pulse': {},
        '/var/lib/dbus': {},
        '/tmp': {},
    },
}

AUDIO_PULSE_USER_V2 = {
    'volume': {
        '/dev/shm': {},
        '/run/pulse': {
            'host': '${HOME}/.pulse/${DBUS_MACHINE_ID}-runtime',
        },
    },
    'environment': {
        'PULSE_SERVER': '/run/pulse/native',
    },
}

AUDIO_PULSE_USER_SHARED = {
    'volume': {
        '/dev/shm': {},
        '/tmp/pulse-socket': {},
    },
}

DISPLAY_X = {
    'environment': {
        'DISPLAY': 'unix${DISPLAY}',
    },
    'volume': {
        '/tmp/.X11-unix': {},
    },
}

LOCALTIME = {
    'volume': {
        '/etc/localtime': {
            'readonly': True
        },
    },
}

VIDEO = {
    'device': {
        '/dev/video0': {},
    },
}

CAPABILITY = {
    'audio': AUDIO_PULSE_USER_V2, #_SHARED,
    'display': DISPLAY_X,
    'localtime': LOCALTIME,
    'video': VIDEO,
}


def image_version(name):
    return 'latest'


class Run(object):
    '''
    Helper class for building 'docker run' arguments.
    '''
    def __init__(self, config, args, env, tty, interactive):
        name = config['name']

        self.docker_cmd = [ 'docker', 'run' ]

        self.docker_args = [ '--name', name ]

        if interactive:
            self.docker_args.append('--interactive')
            self.docker_args.append('--rm')

        if tty:
            self.docker_args.append('--tty')
        else:
            if config.get('option.detach', False):
                self.docker_args.append('--detach')

        for c in config.get('capability', []):
            cap = CAPABILITY[c]
            util.tree_subst_env(cap)
            self.update(cap)

        self.update(config)

        version = image_version(name)
        self.docker_image = [ '{:s}:{:s}'.format(name, version) ]

        self.app_args = args

    @property
    def args(self):
        return self.docker_cmd + self.docker_args + \
            self.docker_image + self.app_args

    def update(self, config):
        self.add_devices(config.get('device', {}))
        self.add_env_vars(config.get('environment', {}))
        self.add_volumes(config.get('volume', {}))

    def add_devices(self, devices):
        for path_container, data in devices.iteritems():
            path_host = os.path.realpath(data.get('host', path_container))
            if os.path.exists(path_host):
                dev = '{:s}:{:s}'.format(path_host, path_container)
                self.docker_args +=  [ '--device', dev ]
            else:
                logging.warn('Host device {:s} not found'.format(path_host))

    def add_env_vars(self, env):
        for k, v in env.iteritems():
            self.docker_args += [ '-e', '{:s}={:s}'.format(k, str(v)) ]

    def add_volumes(self, volumes):
        for path_container, data in volumes.iteritems():
            path_host = os.path.realpath(data.get('host', path_container))
            if os.path.exists(path_host):
                vol = '{:s}:{:s}'.format(path_host, path_container)
                if data.get('readonly', False):
                    vol += ':ro'
                self.docker_args += [ '--volume', vol ]
            else:
                logging.warn('Host path {:s} not found'.format(path_host))


def is_running(name):
    args = [ 'docker', 'inspect', '-f', '"{{ .Name }}"', name ]

    with open(os.devnull, 'w') as devnull:
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=devnull)
        for line in iter(p.stdout.readline, ''):
            if name in line:
                return True

    return False


def restart(name):
    logging.info('Restarting {:s}'.format(name))
    args = [ 'docker', 'restart', name ]
    subprocess.call(args)


def run(config, args, env=None, tty=False, shell=False):
    '''
    Run application described in config, with arguments args.
    '''
    name = config['name']
    logging.info('Running {:s} (arguments [{:s}])'.format(name, ' '.join(args)))

    interactive = False

    if shell is True:
        interactive = True
        tty = True

    r = Run(config, args, env=env, interactive=interactive, tty=tty)

    if shell is True:
        r.docker_args += [ '--entrypoint', '/bin/bash' ]

    logging.info(' '.join(r.args))

    subprocess.call(r.args)


def build(config):
    name = config['name']

    # TODO: add a flag to app.yaml which declares whether the app needs to be
    # run under a particular UID
    uid = os.getuid()

    args = [ 'docker', 'build' ]

    if uid is not None:
        args += [ '--build-arg', 'USER_UID={:s}'.format(str(uid)) ]

    version = image_version(name)
    args += [ '-t', '{:s}:{:s}'.format(name, version) ]

    args.append(os.path.join(dockerapp.PATH_APPS, name))

    logging.info(' '.join(args))

    subprocess.call(args)

