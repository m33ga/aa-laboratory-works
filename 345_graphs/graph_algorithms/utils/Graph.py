import random
import networkx as nx
import numpy as np


class Graph:
    def __init__(self):
        # Dictionary of dictionaries: node -> {neighbor: weight}
        self.graph = {}

    def _convert_from_nx(self, nx_graph, directed=False, weighted=True, allow_negative_weights=False):
        self.graph = {}
        for u, v, data in nx_graph.edges(data=True):
            weight = data.get('weight')
            if weight is None:
                if allow_negative_weights:
                    weight = random.randint(-10, 10)
                else:
                    weight = random.randint(1, 10)
            if u not in self.graph:
                self.graph[u] = {}
            self.graph[u][v] = weight
            if not directed and u != v:
                if v not in self.graph:
                    self.graph[v] = {}
                self.graph[v][u] = weight

    def regular(self, n, degree=3):
        G = nx.random_regular_graph(d=degree, n=n, seed=random.randint(0, 1000))
        self._convert_from_nx(G)

    def complete(self, n):
        G = nx.complete_graph(n)
        self._convert_from_nx(G)

    def sparse(self, n, p=0.1):
        max_attempts = 10
        for attempt in range(max_attempts):
            G = nx.erdos_renyi_graph(n=n, p=p, seed=random.randint(0, 1000))
            if nx.is_connected(G):
                self._convert_from_nx(G)
                return
        G = nx.erdos_renyi_graph(n=n, p=p, seed=random.randint(0, 1000))
        components = list(nx.connected_components(G))
        for i in range(len(components) - 1):
            u = next(iter(components[i]))
            v = next(iter(components[i + 1]))
            G.add_edge(u, v)
        self._convert_from_nx(G)

    def dense(self, n, p=0.8):
        G = nx.erdos_renyi_graph(n=n, p=p, seed=random.randint(0, 1000))
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            for i in range(len(components) - 1):
                u = next(iter(components[i]))
                v = next(iter(components[i + 1]))
                G.add_edge(u, v)
        self._convert_from_nx(G)

    def bipartite(self, n):
        n1 = n // 2
        n2 = n - n1
        G = nx.bipartite.random_graph(n1, n2, p=0.5, seed=random.randint(0, 1000))
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            for i in range(len(components) - 1):
                u = next(iter(components[i]))
                v = next(iter(components[i + 1]))
                G.add_edge(u, v)
        self._convert_from_nx(G)

    def cycle(self, n):
        G = nx.cycle_graph(n)
        self._convert_from_nx(G)

    def with_cyclic_subgraph(self, n):
        G = nx.gnm_random_graph(n=n, m=n + 1, seed=random.randint(0, 1000))
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            for i in range(len(components) - 1):
                u = next(iter(components[i]))
                v = next(iter(components[i + 1]))
                G.add_edge(u, v)
        self._convert_from_nx(G)

    def acyclic(self, n):
        G = nx.random_tree(n=n, seed=random.randint(0, 1000))
        self._convert_from_nx(G)

    def shallow_wide_tree(self, n):
        G = nx.star_graph(range(n))
        self._convert_from_nx(G)

    def deep_narrow_tree(self, n):
        G = nx.path_graph(n)
        self._convert_from_nx(G)

    def with_self_loops(self, n):
        G = nx.erdos_renyi_graph(n=n, p=0.3, seed=random.randint(0, 1000))
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            for i in range(len(components) - 1):
                u = next(iter(components[i]))
                v = next(iter(components[i + 1]))
                G.add_edge(u, v)
        for node in G.nodes:
            if random.random() < 0.2:
                G.add_edge(node, node)
        self._convert_from_nx(G)

    def grid(self, n):
        side = int(np.ceil(np.sqrt(n)))
        G = nx.grid_2d_graph(side, side)
        mapping = {(i, j): i * side + j for i in range(side) for j in range(side)}
        G = nx.relabel_nodes(G, mapping)
        self._convert_from_nx(G)

    def with_negative_weights(self, n):
        G = nx.erdos_renyi_graph(n=n, p=0.5, seed=random.randint(0, 1000))
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            for i in range(len(components) - 1):
                u = next(iter(components[i]))
                v = next(iter(components[i + 1]))
                G.add_edge(u, v)
        self._convert_from_nx(G, allow_negative_weights=True)

    def scale_free(self, n):
        G = nx.barabasi_albert_graph(n=n, m=2, seed=random.randint(0, 1000))
        self._convert_from_nx(G)

    def random(self, n):
        G = nx.erdos_renyi_graph(n=n, p=0.5, seed=random.randint(0, 1000))
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            for i in range(len(components) - 1):
                u = next(iter(components[i]))
                v = next(iter(components[i + 1]))
                G.add_edge(u, v)
        self._convert_from_nx(G)

    def get_graph(self):
        return self.graph

    def get_unweighted_graph(self, use_sets=False):
        unweighted_graph = {}
        for u in self.graph:
            neighbors = list(self.graph[u].keys())
            if use_sets:
                unweighted_graph[u] = set(neighbors)
            else:
                unweighted_graph[u] = neighbors
        return unweighted_graph

    def print_graph(self):
        for u in sorted(self.graph):
            neighbors = ', '.join(f"{v}: {self.graph[u][v]}" for v in sorted(self.graph[u]))
            print(f"{u}: {{{neighbors}}}")