def floyd_warshall(graph, num_nodes):
    dist = [[float('inf')] * num_nodes for _ in range(num_nodes)]
    prev = [[None] * num_nodes for _ in range(num_nodes)]

    for i in range(num_nodes):
        dist[i][i] = 0
        prev[i][i] = None

    for u in range(num_nodes):
        for v, w in graph.get(u, {}).items():
            dist[u][v] = w
            prev[u][v] = u

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    prev[i][j] = prev[k][j]

    return dist, prev
