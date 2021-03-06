from pgmpy.models import BayesianModel
from pgmpy.factors.discrete.CPD import TabularCPD
from pgmpy.inference import VariableElimination
import numpy as np
from scipy.stats import truncnorm

def update(nodes):
    # tim node khong co predecessor
    # n_begin = next(
    #     (node for node in nodes if len(node.predecessor) == 0), None)
    # if not n_begin:
    #     return (False, 'Graph bi lap lai')
    # n_begin.get_samples_cache()
    # return (True, '')
    n_ends = get_end_nodes(nodes)
    if not n_ends:
        return (False, 'Graph bi lap lai')
    for node in n_ends:
        node.get_samples_cache()
    return (True, '')


def get_start_nodes(nodes):
    n_starts = [node for node in nodes if len(node.successors) == 0]
    return n_starts


def get_end_nodes(nodes):
    n_ends = [node for node in nodes if len(node.predecessor) == 0]
    return n_ends


""" Duration Model
"""
""" Knowned Risks """
def calc_two_cpd_network(first, second, control_choice=-1):
    """
    :param first: [] list data
    :param second:[] list data
    :return: None
    """
    model = BayesianModel([('C', 'R')])
    cardC = len(first)
    cardR = len(second)
    cpd_control = TabularCPD(variable='C', variable_card=cardC, values=[first])
    cpd_risk_event = TabularCPD(variable='R', variable_card=cardR,
                                values=second,
                                evidence=['C'],
                                evidence_card=[cardC])
    model.add_cpds(cpd_control, cpd_risk_event)
    print('Risk Event model corrent %s' % repr(model.check_model()))
    infer = VariableElimination(model)
    query = infer.query(['R', ], evidence={'C': control_choice})['R'] if control_choice >= 0 else \
            infer.query(['R', ])['R']
    print("Query %s" % query)

    del model
    del cpd_control
    del cpd_risk_event

    return query.values

def generate_tnormal(mean, var, nmin, nmax):
    rnd = np.random.normal(mean, var, 1)[0]
    if rnd < nmin: rnd=nmin
    if rnd > nmax: rnd=nmax
    return rnd

    # samples = truncnorm.rvs(nmin, nmax,
    #                         loc=mean,
    #                         scale=var,
    #                         size=1)
    # return samples[0]


class ProbTable(object):
    def __init__(self, probs, values):
        self.probs = probs
        self.values = values

    def generate(self, size):
        r = [None]* size
        s = np.random.uniform(low=0.0, high=1.0, size=size)
        s2 = [0]*size
        test = [v for v in self.probs]
        t = 1
        for i in range(len(test))[::-1]:
            t = t - test[i]
            test[i]=t
        print(test)
        n = len(test)
        for i in range(len(s)):
            for j in range(n)[::-1]:
                if s[i] >=test[j]:
                    s2[i]= self.values[j]
                    break
        return s2

class Normal():
    def __init__(self, loc, scale):
        self.loc = loc
        self.scale = scale

    def generate(self, size):
        return np.random.normal(loc=self.loc, scale=self.scale, size=size)



