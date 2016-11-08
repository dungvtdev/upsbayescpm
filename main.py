from mybayes import nodes as nd
from mybayes.cache import *

# if __name__ == '__main__':
nd.set_cache(Cache())
tri = nd.TriangularNode(left=0, mode=2, right=6)
# tri.calc_histogram()
# tri.draw_bar()
tri2 = nd.TriangularNode(left=3, mode=8, right=10)

addnode = nd.AddNode(tri, tri2)
addnode.get_histogram()
addnode.draw_bar()
# tri.draw_bar()
# tri2.draw_bar()
plt.show()
