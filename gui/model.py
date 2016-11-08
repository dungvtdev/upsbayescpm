class Model(object):
    activities = []

    def add_activity(self, activity):
        if activity not in self.activities:
            self.activities.add(activity)


class NodeView(object):
    name = ''
    canvas_items = []
    successors = []
    predecessors = []

    def __init__(self, name):
        self.name = name

    def add_successors(self, *argv):
        if argv:
            sucs = argv
            for suc in sucs:
                if suc not in self.successors:
                    self.successors.append(suc)
                    if self not in suc.predecessors:
                        suc.predecessors.append(self)


class ActivityView(NodeView):
    pass
