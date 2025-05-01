import random
import networkx as nx
import numpy as np


class Graph:
    def __init__(self):
        # Dictionary of dictionaries: node -> {neighbor: weight}
        self.graph = {}

        self.metadata = {
            "name": None,
            "type": None,
            "directed": False,
            "weighted": True,
            "sparse": False,
            "dense": False,
            "tree": False,
            "forest": False,
            "cyclic": False,
            "grid": False,
            "diameter": None,
            "connected": True,
            "disconnected": False,
            "weight_distribution": None,
            "weighted_edges": True,
            "negative_weights": False,
        }

    def add_edge(self, u, v, weight=1):
        """Add a directed edge from u to v with given weight."""
        if u not in self.graph:
            self.graph[u] = {}
        if v not in self.graph:
            self.graph[v] = {}
        self.graph[u][v] = weight

    def add_undirected_edge(self, u, v, weight=1):
        self.add_edge(u, v, weight)
        self.add_edge(v, u, weight)

    def get_unweighted(self, use_sets=False):
        unweighted_graph = {}
        for u in self.graph:
            neighbors = list(self.graph[u].keys())
            if use_sets:
                unweighted_graph[u] = set(neighbors)
            else:
                unweighted_graph[u] = neighbors
        return unweighted_graph

    def to_adj_matrix(self):
        nodes = sorted(self.graph.keys())
        n = len(nodes)
        index_map = {node: i for i, node in enumerate(nodes)}

        adj_matrix = np.full((n, n), np.inf)
        np.fill_diagonal(adj_matrix, 0)

        for u in self.graph:
            for v, w in self.graph[u].items():
                adj_matrix[index_map[u]][index_map[v]] = w
        return adj_matrix

    def generate_sparse(self, num_nodes, edge_prob=0.1, directed=False, weighted=True, weight_range=(1, 10)):
        G = nx.erdos_renyi_graph(num_nodes, edge_prob, directed=directed)
        self._nx_to_graph(G, weighted=weighted, weight_range=weight_range)
        self._update_metadata(
            name="Sparse Erdős–Rényi",
            type="Random Sparse",
            directed=directed,
            weighted=weighted,
            sparse=True,
            connected=nx.is_connected(G.to_undirected()) if not directed else None
        )

    def generate_dense(self, num_nodes, edge_prob=0.9, directed=False, weighted=True, weight_range=(1, 10)):
        G = nx.erdos_renyi_graph(num_nodes, edge_prob, directed=directed)
        self._nx_to_graph(G, weighted=weighted, weight_range=weight_range)
        self._update_metadata(
            name="Dense Erdős–Rényi",
            type="Random Dense",
            directed=directed,
            weighted=weighted,
            dense=True,
            connected=True
        )

    def generate_complete(self, num_nodes, directed=False, weighted=False, weight_range=(1, 10)):
        self.graph.clear()
        for node in range(num_nodes):
            self.graph[node] = {}

        for u in range(num_nodes):
            for v in range(num_nodes):
                if u != v:
                    if not directed and u > v:
                        continue
                    weight = random.randint(*weight_range) if weighted else 1
                    self.graph[u][v] = weight
                    if not directed:
                        self.graph[v][u] = weight

        self._update_metadata(
            name="Complete Graph",
            type="Complete",
            directed=directed,
            weighted=weighted,
            dense=True,
            sparse=False,
            connected=True,
            cyclic=True,
            acyclic=False,
            weight_distribution="random" if weighted else "uniform"
        )

    def generate_tree(self, num_nodes, deep=False, wide=False, weighted=True, weight_range=(1, 10)):
        if wide:
            branching_factor = max(2, num_nodes // 5)
            depth = int(np.log(num_nodes) / np.log(branching_factor))
            G = nx.balanced_tree(branching_factor, depth)
            diameter_type = 'shallow'
        elif deep:
            branching_factor = 2
            depth = int(np.log(num_nodes) / np.log(branching_factor))
            G = nx.balanced_tree(branching_factor, depth)
            diameter_type = 'deep'
        else:
            G = nx.random_tree(num_nodes)
            diameter_type = 'medium'

        self._nx_to_graph(G, weighted=weighted, weight_range=weight_range)
        self._update_metadata(
            name="Random Tree",
            type="Tree",
            directed=False,
            weighted=weighted,
            tree=True,
            acyclic=True,
            diameter=diameter_type,
            connected=True
        )

    def generate_deep_tree(self, num_nodes, weighted=True, weight_range=(1, 10)):
        self.generate_tree(num_nodes, deep=True, weighted=weighted, weight_range=weight_range)
        self._update_metadata(name="Random Deep&Narrow Tree")

    def generate_shallow_tree(self, num_nodes, weighted=True, weight_range=(1, 10)):
        self.generate_tree(num_nodes, wide=True, weighted=weighted, weight_range=weight_range)
        self._update_metadata(name="Random Shallow&Wide Tree")

    def generate_disconnected(self, nodes_per_component=(10, 10), directed=False, weighted=True):
        G = nx.empty_graph(0)
        total_nodes = 0
        for n in nodes_per_component:
            g = nx.fast_gnp_random_graph(n, 0.2)
            mapping = {i: i + total_nodes for i in range(n)}
            G = nx.union(G, nx.relabel_nodes(g, mapping))
            total_nodes += n
        self._nx_to_graph(G, weighted=weighted)
        self._update_metadata(
            name="Disconnected Random",
            type="Disconnected",
            directed=directed,
            weighted=weighted,
            disconnected=True,
            connected=False
        )

    def generate_grid(self, width, height, diagonals=False, weighted=True, weight_range=(1, 10)):
        G = nx.grid_2d_graph(width, height)
        if diagonals:
            for x in range(width):
                for y in range(height):
                    neighbors = []
                    if x < width - 1 and y < height - 1:
                        neighbors.append((x + 1, y + 1))
                    if x > 0 and y < height - 1:
                        neighbors.append((x - 1, y + 1))
                    for dx, dy in neighbors:
                        G.add_edge((x, y), (dx, dy))
        mapping = {(x, y): x * height + y for x, y in G.nodes()}
        G = nx.relabel_nodes(G, mapping)
        self._nx_to_graph(G, weighted=weighted, weight_range=weight_range)
        self._update_metadata(
            name=f"{width}x{height} Grid",
            type="Grid",
            directed=False,
            weighted=weighted,
            grid=True,
            connected=True
        )

    def generate_scale_free(self, num_nodes, directed=False, weighted=True, weight_range=(1, 10)):
        G = nx.barabasi_albert_graph(num_nodes, m=max(1, num_nodes // 10))
        self._nx_to_graph(G, weighted=weighted, weight_range=weight_range)
        self._update_metadata(
            name="Scale-Free",
            type="Scale-Free",
            directed=directed,
            weighted=weighted,
            connected=True
        )

    def generate_cyclic(self, num_nodes, cycles=1, weighted=True, weight_range=(1, 10)):
        G = nx.cycle_graph(num_nodes)
        for _ in range(cycles):
            u, v = random.sample(range(num_nodes), 2)
            G.add_edge(u, v)
        self._nx_to_graph(G, weighted=weighted, weight_range=weight_range)
        self._update_metadata(
            name="Cyclic",
            type="Cyclic",
            directed=False,
            weighted=weighted,
            cyclic=True,
            acyclic=False,
            connected=True
        )

    def generate_acyclic(self, num_nodes, directed=True, weighted=True, weight_range=(1, 10)):
        self.graph.clear()
        nodes = list(range(num_nodes))
        edge_count = int(0.5 * num_nodes * (num_nodes - 1))
        edges = set()
        while len(edges) < edge_count:
            u, v = random.sample(nodes, 2)
            if u != v and u < v:
                edges.add((u, v))
        for u, v in edges:
            w = random.randint(*weight_range) if weighted else 1
            self.graph.setdefault(u, {})[v] = w
        self._update_metadata(
            name="Acyclic Random DAG",
            type="Acyclic",
            directed=directed,
            weighted=weighted,
            acyclic=True,
            cyclic=False,
        )

    def generate_weighted_graph(self, num_nodes, density=0.3, weight_distribution='uniform',
                                negative_weights=False, directed=False):
        edge_prob = density
        G = nx.fast_gnp_random_graph(num_nodes, edge_prob, directed=directed)
        self.graph.clear()
        for u, v in G.edges():
            if weight_distribution == 'uniform':
                w = 1
            elif weight_distribution == 'skewed':
                w = random.choice([1, 1, 1, 1, 10])
            elif weight_distribution == 'local_high':
                w = random.randint(50, 100) if u == 0 or v == 0 else random.randint(1, 10)
            elif weight_distribution == 'random':
                w = random.randint(1, 100)
            elif weight_distribution == 'negative':
                w = random.randint(-10, 10)
            else:
                w = 1
            self.graph.setdefault(u, {})[v] = w
            if not directed:
                self.graph.setdefault(v, {})[u] = w

        self._update_metadata(
            name=f"Weighted ({weight_distribution})",
            type="Weighted",
            directed=directed,
            weighted=True,
            weight_distribution=weight_distribution,
            negative_weights=negative_weights
        )

    def _nx_to_graph(self, nx_graph, weighted=True, weight_range=(1, 10)):
        self.graph.clear()
        for u, v in nx_graph.edges():
            w = random.randint(*weight_range) if weighted else 1
            self.graph.setdefault(u, {})[v] = w
            if not nx_graph.is_directed():
                self.graph.setdefault(v, {})[u] = w

    def _update_metadata(self, **kwargs):
        for k, v in kwargs.items():
            self.metadata[k] = v

    def summary(self):
        print("GRAPH SUMMARY:")
        for key, value in self.metadata.items():
            if value is not None:
                print(f"  {key}: {value}")

    def get_graph(self):
        return {u: dict(neighbors) for u, neighbors in self.graph.items()}

    def get_metadata(self):
        return self.metadata.copy()