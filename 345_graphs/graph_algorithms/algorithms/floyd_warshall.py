def floyd_warshall(graph):
    nodes = list(graph.keys())
    dist = {u: {v: float('inf') for v in nodes} for u in nodes}

    for u in nodes:
        dist[u][u] = 0
        for v, w in graph[u]:
            dist[u][v] = w

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist
