import mybayes as bayes
import numpy as np
from mybayes.influence import ProbTable, Normal
from mybayes.settings import NumberOfSample
from copy import deepcopy


class TempCache(object):
    data = {}
    id_top = 0

    def add(self, item):
        self.id_top+=1
        self.data[self.id_top] = item
        return self.id_top

    def get(self, id):
        return self.data[id]

    def remove(self, id):
        if id and id in self.data:
            del self.data[id]


export_plot_node = None

class Model(object):
    nodes = []
    arcs = []

    def new_model(self):
        bayes.remove_all_network()
        self.nodes = []
        self.arcs = []

        global export_plot_node
        export_plot_node = TempCache()

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
        # print('Build network')
        # bayes.remove_network('test')
        # bayes.new_network('test')
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
                # lf.add_successors(ef)
                lf.set_add_value(70)
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

    def build_and_run(self):
        print('Build and run')
        bayes.remove_network('test')
        bayes.new_network('test')
        self.reset()

        success = self.build_network()
        if success:
            # populate duration first
            for act in self.nodes:
                self.build_duration(act)

            print('update')
            self.run()
        else:
            print('graph khong hop le')


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
        es = bayes.nfact.MaxAddValue(add_value=1)  # 5
        # duration = bayes.nfact.Gaussian(loc=loc, scale=scale)  # 7
        duration = bayes.nfact.TempNode()
        ef = bayes.nfact.Equation(es, duration)  # 8
        lf = bayes.nfact.MaxAddValue(add_value=-1)  # 9
        ls = bayes.nfact.Equation(lf, duration)  # 10
        ls.set_weight([1, -1])

        critical = bayes.nfact.MoreThanNode(lf_node=lf, ef_node=ef)

        node.bayes_nodes = (es, ef, ls, lf, critical, duration)

    def build_duration(self, activity):
        duration = activity.duration_model
        delay_node = self.build_knowned_risk(duration, duration.get_element_by_name('knowned_risk'))
        duration_node = self.build_trade_off(duration, duration.get_element_by_name('trade_off'))
        adjust_node = self.build_unknown_factor(duration, duration.get_element_by_name('unknown_factor'))

        duration_bayes = activity.get_bayes_node('duration')

        n = NumberOfSample
        delays = delay_node.get_samples()
        durations = duration_node.get_samples()
        adjusts = adjust_node.get_samples()

        samples = [(1+delays[i])*durations[i]*adjusts[i] for i in range(n)]

        duration_bayes.set_samples(samples)


    def build_knowned_risk(self, duration, known_risk):
        control = known_risk.get_node('control')
        risk_event = known_risk.get_node('risk_event')
        impact = known_risk.get_node('impact')
        response = known_risk.get_node('response')

        # normalize table
        control_data = control.get_pre_calc_data()
        risk_event_data = risk_event.get_pre_calc_data()
        impact_data = impact.get_pre_calc_data()
        response_data = response.get_pre_calc_data()


        # tinh risk_event
        risk_event_values = bayes.influence.calc_two_cpd_network(control_data, risk_event_data,
                                                            control.choice_index if control.choice_index!=control.MANUAL else -1)

        # build model to run
        # risk_event_node = bayes.nfact.TableNode(values=risk_event_values)
        # risk_event_samples = risk_event_node.get_samples()
        #
        # impact_node = bayes.nfact.TableNode(values=impact.data)
        # impact_samples = impact_node.get_samples()
        #
        # response_node = bayes.nfact.TableNode(values=response.data)
        # response_samples = response_node.get_samples()


        # TODO doi cho nay thanh input
        # calc delay from samples
        step = 1.0/(len(impact_data)+1)
        impact_real_values = [step*(i+1) for i in range(len(impact_data))]   # gia tri cua impact tuong ung voi cac rank

        step = 1.0/(len(risk_event_values)-1)
        risk_event_real_values = [step*i for i in range(len(risk_event_values))] # tu 0...1

        step = 1.0 / (len(response_data))
        response_real_values = [step * (i+1) for i in range(len(response_data))[::-1]]  # tu 1..>0

        n = NumberOfSample

        response_samples = ProbTable(response_data, range(len(response_data))).generate(n)

        if impact.choice_index < 0:
            impact_risk_values=[]
            impact_risk_prob =[]
            impact_prob = impact_data
            risk_prob=risk_event_values
            for i in range(len(impact_prob)):
                for j in range(len(risk_prob)):
                    impact_risk_prob.append(impact_prob[i]*risk_prob[j])
                    impact_risk_values.append(impact_real_values[i]*risk_event_real_values[j])

            impact_risk_samples = ProbTable(impact_risk_prob, impact_risk_values).generate(n)
        else:
            impact_real = impact_real_values[impact.choice_index]
            values = [impact_real*risk_event_real_values[i] for i in range(len(risk_event_values))]
            impact_risk_samples = ProbTable(risk_event_values, values).generate(n)

        delay = [None]*n

        for i in range(n):
            pre_delay = bayes.influence.generate_tnormal(impact_risk_samples[i],0.1,0,1)
            delay[i]= pre_delay*response_real_values[response_samples[i]]

        # tao node de ve histogram
        delay_node = bayes.nfact.TempNode(samples=delay)

        id = export_plot_node.add(('Delay', delay_node))

        known_risk.export_plot.append(id)
        known_risk.output_node = id

        return delay_node

    def build_trade_off(self, duration, trade_off):
        n = NumberOfSample

        resources = trade_off.get_node('resources')
        initial_estimate = trade_off.get_node('initial_estimate')

        if resources.choice_index is not None:
            resources_samples = [resources.choice_index]*n
        else:
            resources_probs= resources.get_pre_calc_data()
            resources_samples = ProbTable(resources_probs, range(len(resources_probs))).generate(n)

        if initial_estimate.choice_value is not None:
            ie_samples = [initial_estimate.choice_value] * n
        else:
            ie_samples = Normal(initial_estimate.get_param('loc'),
                                  initial_estimate.get_param('scale')).generate(n)

        samples =[0] * n

        for i in range(n):
            index = int(resources_samples[i])
            triangle = trade_off.triangle_param_rank[index]
            ie = ie_samples[i]
            samples[i] = np.random.triangular(triangle[0]*ie, triangle[1]*ie, triangle[2]*ie,1)[0]

        # tao node de ve histogram
        duration_node = bayes.nfact.TempNode(samples=samples)

        id = export_plot_node.add(('Duration', duration_node))

        trade_off.export_plot.append(id)
        trade_off.output_node = id

        return duration_node

    def build_unknown_factor(self, duration, unknown_factor):
        from scipy.stats import truncnorm
        adjust = unknown_factor.get_node('adjustment_factor')
        if not adjust.choice_value is None:
            samples = [adjust.choice_value] * NumberOfSample
        else:
            samples = truncnorm.rvs(0,1,
                                  loc=adjust.get_param('loc'),
                                  scale=adjust.get_param('scale'),
                                  size = NumberOfSample)

        # tao node de ve histogram
        adjust_node = bayes.nfact.TempNode(samples=samples)

        id = export_plot_node.add(('AdjustFactor', adjust_node))

        unknown_factor.export_plot.append(id)
        unknown_factor.output_node = id

        return adjust_node




    def dump_data(self):
        return {
            'Model':{
                'Activities':[a.dump_data() for a in self.nodes],
                'Arcs':[arc.dump_data() for arc in self.arcs]
            }
        }

    def read_data(self, json_data):
        activities = json_data['Model']['Activities']
        arcs = json_data['Model']['Arcs']

        self.nodes = []
        self.arcs = []

        for a in activities:
            self.nodes.append(ActivityNodeModel('').read_data(a))

        for arc in arcs:
            self.arcs.append(ArcModel().read_data(arc))

    def reset(self):
        for node in self.nodes:
            node.reset()

class ActivityNodeModel(object):
    name = ''
    node_id = None
    text_id = None
    ui_position = ()
    # (es, ef, ls, lf, duration)
    bayes_nodes = ()
    duration_model = None   # type: DurationNodeModel

    def set_name(self, name):
        self.name = name
        self.duration_model.activity_rename(name)

    def copy(self):
        a = ActivityNodeModel(self.name)
        a.node_id = self.node_id
        a.text_id = self.text_id
        a.ui_position = self.ui_position
        a.duration_model = deepcopy(self.duration_model)
        a.bayes_nodes = self.bayes_nodes
        return a

    def __init__(self, name):
        self.name = name
        self.duration_model = DurationNodeModel(name)

    def get_bayes_node(self, name):
        m = ('es', 'ef', 'ls', 'lf', 'critical', 'duration')
        for i, v in enumerate(m):
            if v == name:
                break
        return self.bayes_nodes[i]

    def replace_duration(self, new_duration):
        self.duration_model = new_duration

    def get_export_nodes(self):
        export = []
        for i,k in enumerate(self.duration_model.element_names_label):
            ids = self.duration_model.get_element(i).export_plot
            for id in ids:
                tnode = export_plot_node.get(id)
                name = '%s-%s' %(k,tnode[0])
                export.append((name, tnode[1]))
        ms = ('es', 'ef', 'ls', 'lf', 'critical', 'duration')
        if self.bayes_nodes:
            for m in ms:
                node = self.get_bayes_node(m)
                export.append((m,node))
        return export

    def dump_data(self):
        return {
            'name':self.name,
            'id':self.node_id,
            'ui_pos':self.ui_position,
            'duration':self.duration_model.dump_data(),
        }

    def read_data(self, json_dict):
        self.name = json_dict['name']
        self.node_id = int(json_dict['id'])
        self.ui_position = json_dict['ui_pos']
        self.duration_model.read_data(json_dict['duration'])

        return self

    def reset(self):
        self.duration_model.reset()
        self.bayes_nodes = ()


class ArcModel(object):
    start_id = None
    end_id = None
    arc_id = None
    start_pos = None
    end_pos = None

    def dump_data(self):
        return [self.start_id, self.end_id]
                #, self.start_pos, self.end_pos]

    def read_data(self, ls):
        self.start_id = ls[0]
        self.end_id = ls[1]
        # self.start_pos = ls[2]
        # self.end_pos = ls[3]

        return self

class DurationNodeModel(object):
    element_names_label=('Knowned Risks', 'Trade Off', 'Unknown Factor')
    element_names = ('knowned_risk', 'trade_off', 'unknown_factor')

    def __init__(self, activity_name):
        self.activity_name = activity_name

        self.elements = [None]*len(self.element_names)

        # create knowned risk
        knowned_risk = KnownedRiskModel(activity_name)
        self.elements[0] = knowned_risk

        # create trade off
        trade_off = TradeOffModel(activity_name)
        self.elements[1] = trade_off

        # create unknown factor
        unknown_factor = UnknownFactorModel(activity_name)
        self.elements[2] = unknown_factor

    def activity_rename(self, name):
        if self.elements:
            for e in self.elements:
                e.activity_rename(name)

    def get_element_label_index(self, name):
        return next(i for i in range(len(self.element_names_label)) if name == self.element_names_label[i])

    def get_element(self, index):
        return self.elements[index]

    def get_element_by_name(self, name):
        id = next(i for i in range(len(self.element_names)) if name == self.element_names[i])
        return self.get_element(id)

    def dump_data(self):
        return [e.dump_data() for e in self.elements]

    def read_data(self, ls):
        for i in range(len(ls)):
            self.elements[i].read_data(ls[i])

    def reset(self):
        for e in self.elements:
            e.reset()


class DurationElement(object):
    def __init__(self, activity_name):
        self.nodes_name_label = []
        self.nodes_name=[]
        self.nodes = []
        self.activity_name = activity_name
        self.export_plot = []
        self.output_node = None         # node dau ra cua element

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

    def dump_data(self):
        return [node.dump_data() for node in self.nodes]

    def read_data(self, ls):
        for i in range(len(ls)):
            self.nodes[i].read_data(ls[i])

    def reset(self):
        for e in self.export_plot:
            export_plot_node.remove(e)
        export_plot_node.remove(self.output_node)
        self.export_plot = []
        self.output_node = None

    def activity_rename(self, name):
        if self.nodes:
            for node in self.nodes:
                s = node.name.split('-')
                node.name = '%s-%s' %(name, s[1])

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

        impact = self.nodes[1]
        impact.set_labels(['Very Low', 'Low', 'Medium', 'High', 'Very Hide'])
        impact.lock_labels = True

class TradeOffModel(DurationElement):

    def __init__(self, activity_name):
        super(TradeOffModel, self).__init__(activity_name)
        self.triangle_param_rank=[
            [1.4, 1.8, 2.5],
            [1, 1.3, 1.5],
            [0.9, 1, 1.2],
            [0.8, 0.9, 1],
            [0.7, 0.75, 0.9]
        ]
        self.nodes_name_label=('Resources', 'Initial Estimate')
        self.nodes_name=('resources', 'initial_estimate')

        n = len(self.nodes_name)
        self.nodes = [None] * n
        n_names = ["%s-%s" %(self.activity_name, self.nodes_name[i])
                   for i in range(len(self.nodes_name))]
        self.nodes[0] = NodeCpdModel(n_names[0])
        self.nodes[0].set_labels(['Very Low', 'Low', 'Medium', 'High', 'Very Hide'])
        self.nodes[0].lock_labels = True

        self.nodes[1] = NodeContinuousInterval(n_names[1], 'normal')


class UnknownFactorModel(DurationElement):

    def __init__(self, activity_name):
        super(UnknownFactorModel, self).__init__(activity_name)
        self.nodes_name_label=('Adjustment Factor',)
        self.nodes_name=('adjustment_factor',)

        n_name = "%s-%s" %(self.activity_name, self.nodes_name[0])
        node = NodeContinuousInterval(n_name,'tnormal01')

        self.nodes = [node,]

class NodeContinuousInterval(object):
    type = {'normal':['loc','scale'], 'tnormal01':['loc','scale']}
    def __init__(self, name, type_string):
        self.name = name
        self.type_string = type_string
        self.param_names = self.type[type_string]
        self.choice_value = None
        self.data = None

    def pre_calc_choice(self):
        raise NotImplementedError()

    def can_pre_choice(self):
        # raise NotImplementedError()
        return True

    def try_set_choice(self, value):
        if value is None:
            self.choice_value = None
        else:
            min, max = self.get_bound()
            if value < min: value = min
            if value > max: value = max
            self.choice_value = value
        return self.choice_value

    def get_bound(self):
        if self.data:
            loc = self.get_param('loc')
            scale = self.get_param('scale')
            return (loc - 3*scale, loc+3*scale)
        else:
            return (0,0)

    def get_columns_label(self):
        return ['Values',]

    def get_rows_label(self):
        return self.param_names

    def get_param(self, name):
        index = next(i for i in range(len(self.param_names)) if self.param_names[i]==name)
        return self.data[index][0]

    def dump_data(self):
        return {
            'model':'NodeContinuousInterval',
            'name': self.name,
            'type_string':self.type_string,
            'choice_value':self.choice_value,
            'data':self.data
        }

    def read_data(self, json_dict):
        self.name = json_dict['name']
        self.type_string = json_dict['type_string']
        self.choice_value = json_dict['choice_value']
        self.data = json_dict['data']
        self.param_names = self.type[self.type_string]

    def get_type_string(self):
        return 'Distribution: %s' % self.type_string

class LabeledNodeModel(object):
    def __init__(self, name, node_id=-1):
        self.name = name
        self.node_id = node_id
        self.labels = []
        self.lock_labels = False

    def set_labels(self, labels):
        self.labels = [x for x in labels if x]


class NodeCpdModel(LabeledNodeModel):
    MANUAL = -1

    def __init__(self, name, node_id=-1):
        super(NodeCpdModel, self).__init__(name, node_id)
        self.evidences = []     # nodeCpdModel
        self.data = []
        self.choice_index = self.MANUAL
        # self.algo_node = None   # node chay thuat toan

    def get_pre_calc_data(self):
        data = deepcopy(self.data)
        if data:
            for j in range(len(data[0])):
                n = len(data)
                tong = sum([data[i][j] for i in range(n)])
                for i in range(n):
                    data[i][j] = data[i][j]/tong

        # format lai neu column == 1
        if len(data[0]) == 1:
            data = [data[i][0] for i in range(len(data))]
        return data

    def can_pre_choice(self):
        return not self.evidences

    def get_table_labels(self):
        if self.evidences:
            # TODO cai nay moi chi chay evidences = 1, mo rong them
            return self.evidences[0].labels
        else:
            return ['Prob',]

    def dump_data(self):
        # self.normalize_data()
        return {'model':'NodeCpdModel',
                'name':self.name,
                'labels':self.labels,
                'data':self.data,
                'choice_index':self.choice_index
                }

    def read_data(self, json_dict):
        self.name = json_dict['name']
        self.labels = json_dict['labels']
        self.data = json_dict['data']
        self.choice_index = int(json_dict['choice_index'])

    def get_type_string(self):
        return 'CPD'




