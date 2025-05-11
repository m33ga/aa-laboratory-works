import numpy as np


def floyd(graph, num_nodes):
    INF = float('inf')
    dist = np.full((num_nodes, num_nodes), INF)
    prev = np.full((num_nodes, num_nodes), -1)

    for i in range(num_nodes):
        dist[i, i] = 0
        prev[i, i] = -1

    for u in range(num_nodes):
        for v, w in graph.get(u, {}).items():
            dist[u, v] = w
            prev[u, v] = u

    for k in range(num_nodes):
        new_dist = np.minimum(dist, dist[:, [k]] + dist[[k], :])
        if np.array_equal(new_dist, dist):
            break
        dist = new_dist

    return dist.tolist(), prev.tolist()
