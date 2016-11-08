# add bayespy dir

import matplotlib.pyplot as plt
import numpy as np

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
            value = self._cache.get(p_name, None)
            return value

        def __setattr__(self, name, value):
            if not self._cache:
                raise Exception('Cache is None')
            p_name = self._get_key_name(name)
            self._cache[p_name] = value


class Node(CacheMixin):
    """ Node
    " Cache: self.histogram, self.samples
    """
    id = None
    NumberOfSample = 10000
    NumberOfBins = 30
    successors = []
    predecessor = []

    def __init__(self, *argv, **kargv):
        self.id = _get_id()
        super(Node, self).__init__(str(self.id))

    def add_successors(self, nodes):
        for node in nodes:
            if node not in self.successors:
                self.successors.append(node)

    def add_predecessor(self, nodes):
        for node in nodes:
            if node not in self.predecessor:
                self.predecessor.append(node)

    def get_histogram(self, recalc=True):
        if not self.cache.histogram or recalc:
            g_samples = self.get_samples()
            # print(g_samples)
            h = plt.hist(g_samples, bins=self.NumberOfBins, normed=True)
            self.cache.histogram = h
        return self.cache.histogram

    def draw_bar(self):
        if not self.cache.histogram:
            self.get_histogram()
        h = self.cache.histogram
        heights = h[0]
        lefts = h[1][:len(h[1]) - 1]
        width = lefts[1] - lefts[0] if len(lefts) > 1 else 0.8
        plt.bar(lefts, heights, width=width)
        plt.show()

    def get_samples_iter(self, number=None):
        n = number if number else self.NumberOfSample
        i = 0
        while i < n:
            yield self.get_samples(1)[0]
            i += 1

    def get_samples_cache(self):
        n = number if number else self.NumberOfSample
        s = self.get_samples(n)
        self.cache.samples = s
        return s

    def get_samples(self, number=None):
        raise NotImplementedError('A Node need implement get_samples')


class TriangularNode(Node):
    left = None
    right = None
    mode = None

    def __init__(self, **kargv):
        self.left = kargv.get('left', 0)
        self.right = kargv.get('right', 2)
        self.mode = kargv.get('mode', 1)
        super(TriangularNode, self).__init__(**kargv)

    def get_samples(self, number=None):
        if not number:
            number = self.NumberOfSample
        return np.random.triangular(self.left, self.mode, self.right, number)


class AddNode(Node):

    def __init__(self, *argv, **kargv):
        self.successors = []
        if argv:
            self.successors = argv
        super(AddNode, self).__init__(**kargv)

    def get_samples(self):
        if not self.successors:
            return []

        n = self.NumberOfSample
        iters = [s.get_samples_iter(n) for s in self.successors]

        samples = [0] * n
        i = 0
        try:
            while(i < n):
                temp = 0
                for it in iters:
                    temp += next(it)
                samples[i] = temp
                i += 1
        except StopIteration:
            pass

        return samples

    # def get_histogram(self, samples=None, bins=None):
    #     samples = self.NumberOfSample if not samples else samples
    #     bins = self.NumberOfBins if not bins else bins
