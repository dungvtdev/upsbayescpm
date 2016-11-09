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


class NodeModel(object):
    name = ''
    node_id = None
    text_id = None
    histogram_nodes = ()

    def __init__(self, name):
        self.name = name


class ArcModel(object):
    start_id = None
    end_id = None
    arc_id = None
    start_pos = None
    end_pos = None
