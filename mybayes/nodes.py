# add bayespy dir

import matplotlib.pyplot as plt
import numpy as np
from . import settings
from .influence import ProbTable

# import math

_cache = None


def set_cache(cache):
    global _cache
    _cache = cache

_id = 0


def _get_id():
    global _id
    id = _id
    _id += 1
    return id


class CacheMixin(object):

    def __init__(self, prefix):
        self.cache = self._Cache(prefix, _cache)

    class _Cache(object):

        def __init__(self, prefix, cache_dict):
            self.__dict__['_cache'] = cache_dict
            self.__dict__['_prefix'] = prefix

        def _get_key_name(self, name):
            return "%s_%s" % (self._prefix, name)

        def __getattr__(self, name):
            if not self._cache:
                raise Exception('Cache is None')
            p_name = self._get_key_name(name)
            if p_name in self._cache:
                return True, self._cache[p_name]
            else:
                return False, None

        def __setattr__(self, name, value):
            if not self._cache:
                raise Exception('Cache is None')
            p_name = self._get_key_name(name)
            self._cache[p_name] = value


class Node(CacheMixin):
    """ Node
    " Cache: self.histogram, self.samples
    """

    def __init__(self, *argv, **kargv):
        self.id = _get_id()
        self.successors = []
        self.predecessor = []
        super(Node, self).__init__(str(self.id))

    def add_successors(self, *nodes):
        for node in nodes:
            if node not in self.successors:
                self.successors.append(node)
                node.add_predecessor([self, ])

    def add_predecessor(self, nodes):
        for node in nodes:
            if node not in self.predecessor:
                self.predecessor.append(node)

    def get_histogram(self, recalc=True):
        cached, cache_hist = self.cache.histogram
        if not cached or recalc:
            g_samples = self.get_samples()
            # print(g_samples)
            h = plt.hist(g_samples, bins=settings.NumberOfBins, normed=True)
            self.cache.histogram = h
            return h
        else:
            return cache_hist

    def draw_bar(self):
        cached, cache_hist = self.cache.histogram
        if not cached:
            cache_hist = self.get_histogram()
        h = cache_hist
        heights = h[0]
        lefts = h[1][:len(h[1]) - 1]
        width = lefts[1] - lefts[0] if len(lefts) > 1 else 0.8
        plt.bar(lefts, heights, width=width)
        plt.show()

    def get_samples_iter(self, number=None):
        n = number if number else settings.NumberOfSample
        i = 0
        while i < n:
            yield self.get_samples(1)[0]
            i += 1

    def get_samples_cache(self):
        cached, cache_samples = self.cache.samples
        if not cached:
            print('Calc samples of node %s' % str(self.id))
            n = settings.NumberOfSample
            cache_samples = self.get_samples(n)
            self.cache.samples = cache_samples
        else:
            print('Hit cache node %s' % str(self.id))
        return cache_samples

    def get_samples(self, number=None):
        raise NotImplementedError('A Node need implement get_samples')


class TriangularNode(Node):

    def __init__(self, **kargv):
        super(TriangularNode, self).__init__(**kargv)
        self.left = kargv.get('left', 0)
        self.right = kargv.get('right', 2)
        self.mode = kargv.get('mode', 1)

    def get_samples(self, number=None):
        if not number:
            number = settings.NumberOfSample
        return np.random.triangular(self.left, self.mode, self.right, number)


class GaussianNode(Node):

    def __init__(self, **kargv):
        super(GaussianNode, self).__init__(**kargv)
        self.loc = kargv.get('loc', 0)
        self.scale = kargv.get('scale', 0.01)

    def get_samples(self, number=None):
        if not number:
            number = settings.NumberOfSample
        return np.random.normal(loc=self.loc, scale=self.scale, size=number)


class TableNode(Node):

    def __init__(self, **kargv):
        super(TableNode, self).__init__(**kargv)
        self.values = kargv['values']

    def get_samples(self, number=None):
        if not number:
            number = settings.NumberOfSample
        prob = ProbTable(self.values, range(len(self.values)))
        return prob.generate(number)

class TempNode(Node):

    def __init__(self, **kargv):
        super(TempNode, self).__init__(*kargv)
        self.cache.samples = kargv['samples']

    def get_samples(self, number=None):
        cached, cache_samples = self.cache.samples
        return cache_samples


class ConstantNode(Node):

    def __init__(self, **kargv):
        super(ConstantNode, self).__init__(**kargv)
        self.value = kargv.get('value', 0)

    def get_samples(self, number=None):
        if not number:
            number = settings.NumberOfSample
        s = [self.value] * number
        return s


class MaxAddValueNode(Node):

    def __init__(self, *argv, **kargv):
        super(MaxAddValueNode, self).__init__(**kargv)
        self.add_value = kargv.get('add_value', 0)
        if argv:
            self.add_successors(*argv)

    def set_add_value(self, value):
        self.add_value = value

    def get_samples(self, number=None):
        if not self.successors:
            return []

        n = settings.NumberOfSample
        # if not number:
        #     n = settings.NumberOfSample
        # else:
        #     n = number
        # TODO sua truong hop ConstantNode de toi uu, k can sinh ra 1 mang
        # sample nua
        succ_samples = [s.get_samples_cache() for s in self.successors]

        samples = [0] * n
        n_succ = len(succ_samples)
        for i in range(n):
            max_v = succ_samples[0][i]
            for j in range(n_succ):
                # sum += succ_samples[j][i]
                value = succ_samples[j][i]
                max_v = value if value > max_v else max_v
            samples[i] = max_v + self.add_value
        return samples


class EquationNode(Node):

    def __init__(self, *argv, **kargv):
        super(EquationNode, self).__init__(**kargv)
        self.weight_map = []
        if argv:
            self.add_successors(*argv)
            self.weight_map = [1] * len(argv)

    def set_weight(self, weights):
        if not weights:
            n = len(self.successors) - len(self.weight_map)
            weights = [1] * n
        else:
            self.weight_map = []
            for w in weights:
                self.weight_map.append(w)

    # def add_successors(self, nodes):
    #     super(EquationNode, self).add_successors(nodes)
    #     # self.weight_map.append([1] * len(nodes))

    def get_samples(self, number=None):
        if not self.successors:
            return []

        n = settings.NumberOfSample
        # if not number:
        #     n = settings.NumberOfSample
        # else:
        #     n = number
        # TODO sua truong hop ConstantNode de toi uu, k can sinh ra 1 mang
        # sample nua
        succ_samples = [s.get_samples_cache() for s in self.successors]

        samples = [0] * n
        n_succ = len(succ_samples)
        for i in range(n):
            sum = 0
            for j in range(n_succ):
                # sum += succ_samples[j][i]
                sum += self.weight_map[j] * succ_samples[j][i]
            samples[i] = sum
        return samples

    # def get_histogram(self, samples=None, bins=None):
    #     samples = settings.NumberOfSample if not samples else samples
    #     bins = self.NumberOfBins if not bins else bins


