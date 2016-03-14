'''
Module which defines a simple tree data structure, based on dict.

Trees are represented as dicts-of-dicts

The module provides the following:
    * Path-based indexing
      t['a.b.c'] instead of t['a']['b']['c']
      If any node is not found, the traversal terminates and returns None.

    * Recursive update

    * Pretty-printing
'''

#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------

PATH_SEP = '.'


#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------

def path_join(*tokens):
    return PATH_SEP.join([str(x) for x in tokens])

def path_split(path):
    return path.split(PATH_SEP)

def is_leaf(t):
    return not isinstance(t, dict)

def set(t, path, value):
    if isinstance(path, str):
        path = path_split(path)

    if path:
        head = path.pop(0)

        if path:
            if not head in t:
                t[head] = dict()

            set(t[head], path, value)

        else:
            t[head] = value

def get(t, path, default = None):
    if isinstance(path, str):
        path = path_split(path)

    if path:
        head = path.pop(0)

        if isinstance(t, dict) and head in t:
            if t:
                return get(t[head], path, default = default)

            return t[head]

        return default

    return t

def delete(t, path):
    if isinstance(path, str):
        path = path_split(path)

    if len(path):
        tail = path.pop()
        head = get(t, path)
        if tail in head:
            del head[tail]

def _to_str(t, level):
    result = ''

    def indent(level):
        return ' ' * 4 * level

    for k,v in t.iteritems():
        result += indent(level) + str(k) + ':\n'

        if is_leaf(v):
            result += indent(level + 1) + str(v)
        else:
            result += _to_str(v, level = level + 1)
            pass

        result += '\n'

    return result.rstrip()

def to_str(t):
    return _to_str(t, level = 0)

def _dfs(t, path, func):
    u = func(path, t)
    t = u or t

    if not is_leaf(t):
        for k, v in t.iteritems():
            t[k] = _dfs(v, path + [k], func)

    return t

def dfs(t, func):
    '''
    Depth-first search

    For each node in the tree, the following call is made:
        func(path, node)
    '''
    return _dfs(t, [], func)


class Tree(object):
    def __init__(self):
        self._data = { }

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def __repr__(self):
        return to_str(self.data)

    def __setitem__(self, key, value):
        set(self.data, key, value)

    def __getitem__(self, key):
        return get(self.data, key)

    def get(self, key, default = None):
        return get(self.data, key, default)

    def set(self, key, value):
        return set(self.data, key, value)

    def dfs(self, func):
        return dfs(self.data, func)

