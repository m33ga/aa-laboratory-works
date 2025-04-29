import random
from collections import defaultdict


def generate_graph(num_nodes, density=0.2, directed=False, weighted=True, connected=True, weight_range=(1, 10)):
    max_edges = num_nodes * (num_nodes - 1) if directed else (num_nodes * (num_nodes - 1)) // 2
    num_edges = max(1, int(density * max_edges))
    if connected and num_edges < num_nodes - 1:
        raise ValueError("Density too low to ensure connectivity.")

    graph = defaultdict(list)
    edges = set()

    def add_edge(u, v):
        weight = random.randint(*weight_range) if weighted else 1
        graph[u].append((v, weight))
        edges.add((u, v))
        if not directed:
            graph[v].append((u, weight))
            edges.add((v, u))

    if connected:
        nodes = list(range(num_nodes))
        random.shuffle(nodes)
        for i in range(1, num_nodes):
            u = nodes[i]
            v = nodes[random.randint(0, i - 1)]
            add_edge(u, v)

    while len(edges) // (1 if directed else 2) < num_edges:
        u, v = random.sample(range(num_nodes), 2)
        if (u, v) not in edges:
            add_edge(u, v)

    for i in range(num_nodes):
        graph[i] = graph.get(i, [])

    return dict(graph)
