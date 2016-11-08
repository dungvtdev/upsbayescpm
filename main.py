import mybayes as mb
from mybayes.cache import *


def test_run():
    mb.new_network('net1')
    tri = mb.nfact.Triangular(left=0, mode=2, right=6)
    # tri.calc_histogram()
    # tri.draw_bar()
    # tri2 = nd.TriangularNode(left=3, mode=8, right=10)
    gauss = mb.nfact.Gaussian(loc=4, scale=1)
    cons = mb.nfact.Constant(value=1)

    addnode = mb.nfact.Equation(tri, gauss, cons)
    addnode.get_histogram()
    addnode.draw_bar()
    # tri.draw_bar()
    # tri2.draw_bar()
    plt.show()


def test_simple():
    mb.new_network('net2')
    # action a
    es_a = mb.nfact.Constant(value=0)  # 0
    print(es_a)
    d_a = mb.nfact.Gaussian(loc=5, scale=1)  # 1
    ef_a = mb.nfact.Equation(es_a, d_a)  # 2
    ls_a = mb.nfact.Equation()  # 3
    lf_a = mb.nfact.Equation()  # 4

    # action b
    es_b = mb.nfact.Equation(ef_a, mb.nfact.Constant(value=1))  # 5
    d_b = mb.nfact.Gaussian(loc=10, scale=2)  # 7
    ef_b = mb.nfact.Equation(es_b, d_b)  # 8
    lf_b = mb.nfact.Equation(ef_b)  # 9
    ls_b = mb.nfact.Equation(lf_b, d_b)  # 10
    ls_b.set_weight([1, -1])

    lf_a.add_successors(ls_b, mb.nfact.Constant(value=1))  # 11
    lf_a.set_weight([1, -1])
    ls_a.add_successors(lf_a, d_a)
    ls_a.set_weight([1, -1])

    mb.update()

    ef_b.get_histogram()
    ef_b.draw_bar()
    plt.show()


if __name__ == '__main__':
    mb.set_cache(Cache())
    test_simple()
