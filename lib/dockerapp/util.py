'''
Utility module.
'''

def json_pretty(data):
    import json
    return json.dumps(data, indent=4, sort_keys=True)

def yaml_pretty(data):
    import yaml
    return yaml.safe_dump(data, indent=4, default_flow_style=False)

def import_module(name):
    def _import(name):
        m = __import__(name)
        for n in name.split(".")[1:]:
            m = getattr(m, n)
        return m

    return _import(name)

def tree_subst_env(data, env=None):
    import os
    import re
    from dockerapp import tree

    e = os.environ
    if env is not None:
        e.update(env)
    env = e

    def replace(m):
        key = m.group(0)[2:-1]
        return str(e.get(key, ''))

    def visit(path, node):
        if isinstance(node, basestring):
            return re.subn(r'(\$\{[a-zA-Z_]+\})', replace, node)[0]

    tree.dfs(data, visit)

