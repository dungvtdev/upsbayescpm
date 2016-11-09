import mybayes as bayes


class Model(object):
    nodes = []
    arcs = []

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def add_arc(self, arc):
        if arc not in self.arcs:
            self.arcs.append(arc)

    def remove_node(self, node):
        if isinstance(node, NodeModel):
            self.nodes.remove(node)
        else:
            id = node
            node = self.get_node(id)
            if node:
                self.nodes.remove(node)

    def remove_arc(self, arc):
        if isinstance(arc, ArcModel):
            self.arcs.remove(arc)
        else:
            id = arc
            arc = self.get_arc(id)
            if arc:
                self.arcs.remove(arc)

    def get_arc(self, id):
        return next((a for a in self.arcs if a.arc_id == id), None)

    def get_node(self, id):
        return next((n for n in self.nodes if n.node_id == id), None)

    def is_node(self, id):
        nd = self.get_node(id)
        return True if nd else False

    def get_arcs_attach_node(self, node_id):
        arcs = [a for a in self.arcs if (
            a.start_id == node_id or a.end_id == node_id)]
        if arcs and len(arcs):
            return arcs

    def build_network(self):
        print('Build network')
        bayes.remove_network('test')
        bayes.new_network('test')
        # create nodes
        for node in self.nodes:
            self.create_action(node)
        # populate link
        for arc in self.arcs:
            self.populate_arc(arc)
        # start and end
        succes_set = set([arc.end_id for arc in self.arcs])
        pre_set = set([arc.start_id for arc in self.arcs])
        full_set = set([node.node_id for node in self.nodes])

        end_set = full_set - pre_set
        start_set = full_set - succes_set

        if end_set and start_set:
            for end_node_id in end_set:
                node = self.get_node(end_node_id)
                ef = node.get_bayes_node('ef')
                lf = node.get_bayes_node('lf')
                lf.add_successors(ef)
                lf.set_weight([1, ])
            for start_node_id in start_set:
                node = self.get_node(start_node_id)
                es = node.get_bayes_node('es')
                es.add_successors(bayes.nfact.Constant(value=0))
                es.set_weight([1, ])
            return True
        else:
            return False

    def run(self):
        bayes.update()

    def populate_arc(self, arc):
        start = self.get_node(arc.start_id)
        end = self.get_node(arc.end_id)
        if start and end:
            end_es = end.get_bayes_node('es')
            start_ef = start.get_bayes_node('ef')
            end_es.add_successors(start_ef, bayes.nfact.Constant(value=1))
            end_es.set_weight([1, 1])
            start_lf = start.get_bayes_node('lf')
            end_ls = end.get_bayes_node('ls')
            start_lf.add_successors(end_ls, bayes.nfact.Constant(value=1))
            start_lf.set_weight([1, -1])

    def create_action(self, node):
        loc = node.data['normal'][0]
        scale = node.data['normal'][1]

        es = bayes.nfact.Equation()  # 5
        duration = bayes.nfact.Gaussian(loc=loc, scale=scale)  # 7
        ef = bayes.nfact.Equation(es, duration)  # 8
        lf = bayes.nfact.Equation()  # 9
        ls = bayes.nfact.Equation(lf, duration)  # 10
        ls.set_weight([1, -1])

        node.bayes_nodes = (es, ef, ls, lf, duration)


class NodeModel(object):
    name = ''
    node_id = None
    text_id = None
    # (es, ef, ls, lf, duration)
    bayes_nodes = ()
    data = {'normal': (5, 1)}

    def __init__(self, name):
        self.name = name

    def get_bayes_node(self, name):
        m = ('es', 'ef', 'ls', 'lf', 'duration')
        for i, v in enumerate(m):
            if v == name:
                break
        return self.bayes_nodes[i]


class ArcModel(object):
    start_id = None
    end_id = None
    arc_id = None
    start_pos = None
    end_pos = None
