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
