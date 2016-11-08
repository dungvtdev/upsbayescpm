def update(nodes):
    # tim node khong co predecessor
    n_begin = next(
        (node for node in nodes if len(node.predecessor) == 0), None)
    if not n_begin:
        return (False, 'Graph bi lap lai')
    n_begin.get_samples_cache()
    return (True, '')
