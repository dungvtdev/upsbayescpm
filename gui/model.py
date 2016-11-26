import mybayes as bayes


class Model(object):
    nodes = []
    arcs = []

    def replace_node(self, node, new_node):
        self.remove_node(node)
        self.add_node(new_node)

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def add_arc(self, arc):
        if arc not in self.arcs:
            self.arcs.append(arc)

    def remove_node(self, node):
        if isinstance(node, ActivityNodeModel):
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
                lf.set_add_value(0)
                # lf.set_weight([1, ])
            for start_node_id in start_set:
                node = self.get_node(start_node_id)
                es = node.get_bayes_node('es')
                es.add_successors(bayes.nfact.Constant(value=0))
                es.set_add_value(0)
                # es.set_weight([1, ])
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
            end_es.add_successors(start_ef)  # , bayes.nfact.Constant(value=1))
            # end_es.set_weight([1, 1])
            start_lf = start.get_bayes_node('lf')
            end_ls = end.get_bayes_node('ls')
            start_lf.add_successors(end_ls)  # , bayes.nfact.Constant(value=1))
            # start_lf.set_weight([1, -1])

    def create_action(self, node):
        loc = node.data['normal'][0]
        scale = node.data['normal'][1]

        es = bayes.nfact.MaxAddValue(add_value=1)  # 5
        duration = bayes.nfact.Gaussian(loc=loc, scale=scale)  # 7
        ef = bayes.nfact.Equation(es, duration)  # 8
        lf = bayes.nfact.MaxAddValue(add_value=-1)  # 9
        ls = bayes.nfact.Equation(lf, duration)  # 10
        ls.set_weight([1, -1])

        node.bayes_nodes = (es, ef, ls, lf, duration)


class ActivityNodeModel(object):
    name = ''
    node_id = None
    text_id = None
    # (es, ef, ls, lf, duration)
    bayes_nodes = ()
    duration_model = None   # type: DurationNodeModel

    def __init__(self, name):
        self.name = name
        self.duration_model = DurationNodeModel(name)

    def get_bayes_node(self, name):
        m = ('es', 'ef', 'ls', 'lf', 'duration')
        for i, v in enumerate(m):
            if v == name:
                break
        return self.bayes_nodes[i]

    def replace_duration(self, new_duration):
        self.duration_model = new_duration


class ArcModel(object):
    start_id = None
    end_id = None
    arc_id = None
    start_pos = None
    end_pos = None


class DurationNodeModel(object):
    element_names_label=('Knowned Risks',)
    element_names = ('knowned_risk',)

    def __init__(self, activity_name):
        self.activity_name = activity_name

        self.elements = [None]*len(self.element_names)

        # create knowned risk
        knowned_risk = KnownedRiskModel(activity_name)
        self.elements[0] = knowned_risk

    def get_element_label_index(self, name):
        return next(i for i in range(len(self.element_names_label)) if name == self.element_names_label[i])

    def get_element(self, index):
        return self.elements[index]


class DurationElement(object):
    def __init__(self, activity_name):
        self.nodes_name_label = []
        self.nodes_name=[]
        self.nodes = []
        self.activity_name = activity_name

    def get_node_index_by_name(self, name):
        return next((i for i in range(len(self.nodes_name)) if self.nodes_name[i] == name))

    def set_node(self, name, node):
        index = self.get_node_index_by_name(name)
        self.nodes[index] = node

    def get_node(self, name):
        index = self.get_node_index_by_name(name)
        return self.nodes[index]

    def get_node_by_id(self, id):
        return self.nodes[id]


class KnownedRiskModel(DurationElement):
    # self.control = None     # Cpd
    # self.impact = None      # Value
    # self.risk_event = None   # Cpd
    # self.resource = None    # Value
    def __init__(self, activity_name):
        super(KnownedRiskModel, self).__init__(activity_name)
        self.nodes_name_label=('Control', 'Impact', 'Risk Event', 'Response')
        self.nodes_name =('control', 'impact', 'risk_event', 'response')
        self.nodes = [None] * len(self.nodes_name)
        for i in range(len(self.nodes_name)):
            n_name = "%s-%s" %(self.activity_name, self.nodes_name[i])
            self.nodes[i]= NodeCpdModel(n_name)

        # link control va risk_event
        control = self.get_node('control')
        risk_event = self.get_node('risk_event')
        risk_event.evidences = [control,]


class LabeledNodeModel(object):
    def __init__(self, name, node_id=-1):
        self.name = name
        self.node_id = node_id
        self.labels = []

    def set_labels(self, labels):
        self.labels = [x for x in labels if x]


class NodeCpdModel(LabeledNodeModel):

    def __init__(self, name, node_id=-1):
        super(NodeCpdModel, self).__init__(name, node_id)
        self.evidences = []     # nodeCpdModel
        self.data = []

    def get_table_labels(self):
        if self.evidences:
            # TODO cai nay moi chi chay evidences = 1, mo rong them
            return self.evidences[0].labels
        else:
            return ['Prob',]




