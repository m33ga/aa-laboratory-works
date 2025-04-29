import csv
from ..utils.graph_generator import generate_graph
from ..utils.timer import time_function
from ..algorithms import dfs, bfs, prim, kruskal, dijkstra, floyd_warshall


def run_benchmark(algorithm_batch, node_sizes, densities, repetitions=2, directed=False, weighted=True):
    results = []

    algorithm_batches = {
        "Traversal": {"DFS": dfs, "BFS": bfs},
        "MST": {"Prim": prim, "Kruskal": kruskal},
        "ShortestPaths": {"Dijkstra": dijkstra, "FloydWarshall": floyd_warshall}
    }

    for num_nodes in node_sizes:
        for density in densities:
            for _ in range(repetitions):
                graph = generate_graph(num_nodes, density=density, directed=directed, weighted=weighted)

                for name, algo in algorithm_batches[algorithm_batch].items():
                    if name in ["DFS", "BFS", "Dijkstra"]:
                        args = (graph, 0)
                    else:
                        args = (graph,)

                    elapsed, _ = time_function(algo, *args)
                    results.append({
                        "algorithm": name,
                        "nodes": num_nodes,
                        "density": density,
                        "time": elapsed
                    })
    return results


def save_results_to_csv(results, filename):
    keys = results[0].keys()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
