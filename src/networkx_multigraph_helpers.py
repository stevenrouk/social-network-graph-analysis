def get_edge_attrs(graph, node1, node2):
    return dict(graph[node1][node2].items())

def aggregate_numeric_properties(graph, node1, node2, numeric_attrs, agg_func):
    attr_dict = get_edge_attrs(graph, node1, node2)
    aggregated_dict = {attr: [] for attr in numeric_attrs}
    for edge in attr_dict:
        for attr in numeric_attrs:
            aggregated_dict[attr].append(attr_dict[edge]['attr'][attr])
    
    for k in aggregated_dict:
        aggregated_dict[k] = agg_func(aggregated_dict[k])
    
    return aggregated_dict

def sum_numeric_properties(graph, node1, node2, numeric_attrs):
    """For now, this function just calls aggregate_numeric_properties.
    However, the original code is below if this turns out to be inefficient.
    
    attr_dict = get_edge_attrs(graph, node1, node2)
    summed_dict = {attr: 0 for attr in numeric_attrs}
    for edge in attr_dict:
        for attr in numeric_attrs:
            summed_dict[attr] += attr_dict[edge]['attr'][attr]
    
    return summed_dict
    """
    return aggregate_numeric_properties(graph, node1, node2, numeric_attrs, sum)

def count_edges(graph, node1, node2):
    return len(graph[node1][node2])

def sharing_reciprocity(graph, n, m):
    try:
        n_to_m = graph[n][m]['weight']
    except:
        n_to_m = 0
    
    try:
        m_to_n = graph[m][n]['weight']
    except:
        m_to_n = 0
    
    if n_to_m + m_to_n == 0:
        return 0
    
    return {
        'reciprocity': n_to_m / (n_to_m + m_to_n),
        'summed weights': n_to_m + m_to_n,
        'n-to-m': n_to_m,
        'm_to_n': m_to_n
    }