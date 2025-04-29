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
