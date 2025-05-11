from graph_algorithms.utils.Graph import Graph
from graph_algorithms.algorithms import dfs, bfs, dijkstra, floyd_warshall, prim, kruskal
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import time


def plot_results(res, num_nodes_lst, title):
    plt.figure()
    for algo_name, res_lst in res.items():
        plt.plot(num_nodes_lst, res_lst, label=algo_name)

    plt.legend()
    plt.title(title)
    plt.grid()
    plt.xlabel("num of nodes")
    plt.ylabel("time")
    plt.show()


def benchmark(graph_name, graph_gen, graph_sizes, algo1, algo2, algo3, algo4, algo5, algo6):

    results12 = {
        algo1.__name__: [],
        algo2.__name__: [],
    }

    results34 = {
        algo3.__name__: [],
        algo4.__name__: [],
    }

    results56 = {
        algo5.__name__: [],
        algo6.__name__: [],
    }

    for size in graph_sizes:
        g = Graph()

        graph_gen(g, size)
        graph_unw = g.get_unweighted_graph()
        graph = g.get_graph()
        num_nodes = len(graph.keys())

        timer, _ = time_function(algo1, graph_unw, num_nodes)
        results12[algo1.__name__].append(timer)

        timer, _ = time_function(algo2, graph_unw, num_nodes)
        results12[algo2.__name__].append(timer)

        timer, _ = time_function(algo3, graph, num_nodes)
        results34[algo3.__name__].append(timer)

        timer, _ = time_function(algo4, graph, num_nodes)
        results34[algo4.__name__].append(timer)

        timer, _ = time_function(algo5, graph, num_nodes)
        results56[algo5.__name__].append(timer)

        timer, _ = time_function(algo6, graph, num_nodes)
        results56[algo6.__name__].append(timer)

    plot_results(results12, graph_sizes, f"{algo1.__name__.upper()} and {algo2.__name__.upper()} on {graph_name} graph")
    plot_results(results34, graph_sizes, f"{algo3.__name__.upper()} and {algo4.__name__.upper()} on {graph_name} graph")
    plot_results(results56, graph_sizes, f"{algo5.__name__.upper()} and {algo6.__name__.upper()} on {graph_name} graph")
    return results12, results34, results56


graph_generators = {
    "Sparse": lambda g, size: g.sparse(size),
    "Dense": lambda g, size: g.dense(size),
    "Regular": lambda g, size: g.regular(size),
    "Bipartite": lambda g, size: g.bipartite(size),
    "Tree Deep": lambda g, size: g.deep_narrow_tree(size),
    "Tree Shallow": lambda g, size: g.shallow_wide_tree(size),
    "Grid": lambda g, size: g.grid(size),
    "Cycle": lambda g, size: g.cycle(size),
    "With Sub-Cycle": lambda g, size: g.with_cyclic_subgraph(size),
    "With Self-Loops": lambda g, size: g.with_self_loops(size),
    "Acyclic": lambda g, size: g.acyclic(size),
    "Complete": lambda g, size: g.complete(size),
    "Negative Weight": lambda g, size: g.with_negative_weights(size),
    "Scale Free": lambda g, size: g.scale_free(size),
    "Random": lambda g, size: g.random(size),
}

sizes = [10, 100, 200, 300, 500]
table = PrettyTable()

for name, gen in graph_generators.items():
    benchmark(name, gen, sizes, bfs, dfs, dijkstra, floyd_warshall, prim, kruskal)
