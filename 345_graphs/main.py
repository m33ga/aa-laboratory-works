from graph_algorithms.benchmark import run_benchmark, save_results_to_csv, plot_all_batches


node_sizes = [50, 100, 200]
densities = [0.1, 0.9]  # sparse and dense
repetitions = 3
algorithm_batches = ["Traversal", "MST", "ShortestPaths"]

for batch in algorithm_batches:
    print(f"processing {batch} algorithms")
    results = run_benchmark(
        algorithm_batch=batch,
        node_sizes=node_sizes,
        densities=densities,
        repetitions=repetitions
    )
    csv_file = f"{batch.lower()}_results.csv"
    save_results_to_csv(results, csv_file)

plot_all_batches()
