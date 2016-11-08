# add bayespy dir
import init_utils

import numpy as np
import matplotlib.pyplot as plt


class Node(object):
    NumberOfSample = 10000
    NumberOfBins = 30
    histogram = None
    successors = []
    predecessor = []

    def add_successors(self, node):
        if node not in self.successors:
            self.successors.append(node)

    def add_predecessor(self, node):
        if node not in self.predecessor:
            self.predecessor.append(node)

    def calc_histogram(self, recalc=True, samples=None, bins=None):
        if not self.histogram or recalc:
            self.NumberOfSample = samples if samples else self.NumberOfSample
            self.NumberOfBins = bins if bins else self.NumberOfBins
            g_samples = self.get_samples()
            # print(g_samples)
            h = plt.hist(g_samples, bins=self.NumberOfBins, normed=True)
            self.histogram = h
        return self.histogram

    def draw_bar(self):
        if not self.histogram:
            self.calc_histogram()
        heights = self.histogram[0]
        lefts = self.histogram[1][:len(self.histogram[1]) - 1]
        width = lefts[1] - lefts[0] if len(lefts) > 1 else 0.8
        plt.bar(lefts, heights, width=width)
        plt.show()

    def get_samples_lazy(self, number=None):
        n = number if number else self.NumberOfSample
        i = 0
        while i < n:
            yield self.get_samples(1)[0]
            i += 1

    def get_samples(self, number=None):
        raise NotImplementedError('A Node need implement get_samples')


class TriangularNode(Node):

    def __init__(self, **kargv):
        self.left = kargv.setdefault('left', 0)
        self.right = kargv.setdefault('right', 2)
        self.mode = kargv.setdefault('mode', 1)

    def get_samples(self, number=None):
        if not number:
            number = self.NumberOfSample
        return np.random.triangular(self.left, self.mode, self.right, number)


class AddNode(Node):

    def __init__(self, *argv):
        self.successors = argv

    def get_samples(self):
        if not self.successors:
            return []

        n = self.NumberOfSample
        iters = [s.get_samples_lazy(n) for s in self.successors]

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


if __name__ == '__main__':
    tri = TriangularNode(left=0, mode=2, right=6)
    # tri.calc_histogram()
    # tri.draw_bar()
    tri2 = TriangularNode(left=3, mode=8, right=10)

    addnode = AddNode(tri, tri2)
    addnode.calc_histogram()
    addnode.draw_bar()
    # tri.draw_bar()
    # tri2.draw_bar()
    plt.show()
