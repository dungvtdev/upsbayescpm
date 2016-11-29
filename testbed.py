from pgmpy.models import BayesianModel
from pgmpy.factors.discrete.CPD import TabularCPD
from pgmpy.inference import VariableElimination

def calc_risk_event(control_data, risk_event_data, control_choice=-1):
    """
    :param control_data: [] list data
    :param risk_event_data:[] list data
    :return: None
    """
    model = BayesianModel([('C', 'R')])
    cardC = len(control_data)
    cardR = len(risk_event_data)
    cpd_control = TabularCPD(variable='C', variable_card=cardC, values=[control_data])
    cpd_risk_event = TabularCPD(variable='R', variable_card=cardR,
                                values=risk_event_data,
                                evidence=['C'],
                                evidence_card=[cardC])
    model.add_cpds(cpd_control, cpd_risk_event)
    print('Risk Event model corrent %s' % repr(model.check_model()))
    infer = VariableElimination(model)
    query = infer.query(['R', ], evidence={'C': control_choice})['R'] if control_choice >= 0 else \
            infer.query(['R', ])['R']
    print("Query %s" % query)
    return query.values

def test_table_prob():
    from mybayes.influence import ProbTable
    values = [1,3,4]
    probs = [0.2, 0.3,0.5]
    prob = ProbTable(probs, values)
    print(prob.generate(50))

if __name__ == '__main__':
    # main()
    control_data = [0.6,0.15, 0.25]
    risk_event_data = [[0.3, 0.8, 0.25], [0.7, 0.2, 0.75]]
    calc_risk_event(control_data, risk_event_data, 0)
    # test_table_prob()