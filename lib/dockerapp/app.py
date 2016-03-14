'''
Application.
'''

import logging
import os

import dockerapp
from dockerapp import tree
from dockerapp import util

class Config(tree.Tree):
    def __init__(self, name, env=None):
        super(Config, self).__init__()
        self._read(name)

        util.tree_subst_env(self.data)

        logging.debug(self)

    def _read(self, name):
        path_app = os.path.join(dockerapp.PATH_APPS, name)
        path_config = os.path.join(path_app, 'app.yaml')

        with open(path_config) as f:
            import yaml
            data = yaml.load(f)

        self._validate(data)

        self.data = data

        self['name'] = name

    def _validate(self, data):
        path_schema = os.path.join(dockerapp.PATH_SCHEMA, 'app.json')
        with open(path_schema) as f:
            import json
            schema = json.load(f)
            import jsonschema
            jsonschema.validate(data, schema)

