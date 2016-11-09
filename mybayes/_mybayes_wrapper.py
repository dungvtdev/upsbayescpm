from . import nodes as nd
from . import influence

_network = {}
_name = None


def set_cache(cache):
    nd.set_cache(cache)


def new_network(name):
    if name in _network.keys():
        raise ValueError('Name %s is defined, choose another name' % name)
    _network[name] = []
    set_network(name)


def set_network(name):
    if name not in _network.keys():
        raise ValueError('Name %s chua define, k dung duoc' % name)
    global _name
    _name = name


def remove_network(name):
    if name in _network.keys():
        # raise ValueError('Name %s chua define, k xoa duoc' % name)
        del _network[name]


def _get_network():
    return _network[_name]


def update():
    success, msg = influence.update(_get_network())
    print('Success %s %s' % (str(success), msg))


class _NodeFactory(object):
    names = {'Gaussian': nd.GaussianNode,
             'Triangular': nd.TriangularNode,
             'Constant': nd.ConstantNode,
             'Equation': nd.EquationNode, }

    def __getattr__(self, name):
        m_node = self.names.get(name, None)
        if m_node:
            def func(*argv, **kargv):
                inst = m_node(*argv, **kargv)
                c_network = _get_network()
                c_network.append(inst)
                return inst
            return func
        else:
            return None

nfact = _NodeFactory()
