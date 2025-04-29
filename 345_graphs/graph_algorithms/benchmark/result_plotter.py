import csv
import matplotlib.pyplot as plt
from collections import defaultdict


def load_results(filename):
    data = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                "algorithm": row["algorithm"],
                "nodes": int(row["nodes"]),
                "density": float(row["density"]),
                "time": float(row["time"])
            })
    return data


def group_results_by_density(data, sparse_threshold=0.3):
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for row in data:
        alg = row["algorithm"]
        nodes = row["nodes"]
        density_group = "sparse" if row["density"] <= sparse_threshold else "dense"
        grouped[alg][density_group][nodes].append(row["time"])
    return grouped


def average(values):
    return sum(values) / len(values) if values else 0


def plot_algorithm_group(data, title, algorithms):
    grouped = group_results_by_density(data)

    plt.figure()
    for alg in algorithms:
        for density_group in ["sparse", "dense"]:
            nodes = sorted(grouped[alg][density_group].keys())
            times = [average(grouped[alg][density_group][n]) for n in nodes]
            label = f"{alg} ({density_group})"
            plt.plot(nodes, times, marker="o", label=label)

    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (s)")
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def plot_all_batches():
    plot_algorithm_group(
        load_results("traversal_results.csv"),
        title="DFS vs BFS (Traversal Algorithms)",
        algorithms=["DFS", "BFS"]
    )

    plot_algorithm_group(
        load_results("mst_results.csv"),
        title="Prim vs Kruskal (MST Algorithms)",
        algorithms=["Prim", "Kruskal"]
    )

    plot_algorithm_group(
        load_results("shortestpaths_results.csv"),
        title="Dijkstra vs Floyd-Warshall (Shortest Path Algorithms)",
        algorithms=["Dijkstra", "FloydWarshall"]
    )

