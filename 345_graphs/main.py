import numpy as np

from graph_algorithms.utils.Graph import Graph
from graph_algorithms.utils.timer import time_function
from graph_algorithms.algorithms import dfs, bfs, dijkstra, floyd, prim, kruskal
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import os

SAVE_DIR = "benchmark_figures"
os.makedirs(SAVE_DIR, exist_ok=True)


def plot_results(res, num_nodes_lst, title, graph_name, colors=plt.cm.tab10.colors):
    plt.figure(figsize=(10, 6))

    file_name = ""

    for idx, (algo_name, res_lst) in enumerate(res.items()):
        file_name += f"{algo_name}_"
        color = colors[idx % len(colors)]
        plt.plot(num_nodes_lst, res_lst, label=algo_name, color=color, linewidth=2)

    file_name += graph_name.replace(" ", "_")
    file_path = os.path.join(SAVE_DIR, file_name)

    plt.title(title)
    plt.xlabel("Number of Nodes", fontsize=12)
    plt.ylabel("Execution Time (seconds)", fontsize=12)
    plt.xticks(num_nodes_lst)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10, loc='best')
    plt.tight_layout()
    plt.savefig(file_path + ".png", dpi=300, bbox_inches='tight')
    plt.close()


def print_table(results, algos, sizes):
    table = PrettyTable()
    table.clear()
    table.title = f"{algos[0].upper()} and {algos[1].upper()} comparison"
    table.field_names = ["Graph Type\\Nr of nodes"] + [str(s) + f" ({algo.upper()})" for s in sizes for algo in algos]

    for graph, res in results.items():
        row = [graph]
        for i in range(len(sizes)):
            for algo in algos:
                for d in res:
                    if algo in d.keys():
                        row.append(f"{d[algo][i]:.6f}")
        table.add_row(row)

    print(table)


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

    colors = plt.cm.tab10.colors
    plot_results(results12, graph_sizes, f"{algo1.__name__.upper()} and {algo2.__name__.upper()} on {graph_name} graph", graph_name, colors=colors[0:2])
    plot_results(results34, graph_sizes, f"{algo3.__name__.upper()} and {algo4.__name__.upper()} on {graph_name} graph", graph_name, colors=colors[2:4])
    plot_results(results56, graph_sizes, f"{algo5.__name__.upper()} and {algo6.__name__.upper()} on {graph_name} graph", graph_name, colors=colors[4:6])
    return results12, results34, results56


def print_aggregated_results(results, sizes):
    aggregated_results = {}
    graph_num = 0
    for g_type, g_res in results.items():
        graph_num += 1
        for batch_dict in g_res:
            for algo, algo_res in batch_dict.items():
                if algo not in aggregated_results.keys():
                    aggregated_results[algo] = np.array(algo_res)
                else:
                    aggregated_results[algo] += np.array(algo_res)
    for algo, res in aggregated_results.items():
        aggregated_results[algo] /= graph_num

    table = PrettyTable()
    table.clear()
    table.title = "Aggregated results"
    table.field_names = ["Algo"] + [str(s) for s in sizes]

    for algo, res in aggregated_results.items():
        row = [algo]
        for item in res:
            row.append(f"{item:.6f}")
        table.add_row(row)

    print(table)


def main():
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
        "Directed": lambda g, size: g.directed(size),
        "Random": lambda g, size: g.random(size),
    }

    sizes = [20, 100, 200, 300, 450, 600, 1000]
    results = {}

    for name, gen in graph_generators.items():
        results[name] = benchmark(name, gen, sizes, bfs, dfs, dijkstra, floyd, prim, kruskal)

    print_table(results, algos=['bfs', 'dfs'], sizes=sizes)
    print_table(results, algos=['dijkstra', 'floyd'], sizes=sizes)
    print_table(results, algos=['prim', 'kruskal'], sizes=sizes)

    print_aggregated_results(results=results, sizes=sizes)


if __name__ == '__main__':
    main()
