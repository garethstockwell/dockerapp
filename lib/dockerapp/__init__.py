# dockerapp

import os

__path_self = os.path.dirname(os.path.abspath(__file__))

PATH_BASE = os.path.abspath(os.path.join(
    __path_self,
    os.path.pardir,
    os.path.pardir))

PATH_APPS = os.path.join(PATH_BASE, 'apps')
PATH_SCHEMA = os.path.join(PATH_BASE, 'schema')

