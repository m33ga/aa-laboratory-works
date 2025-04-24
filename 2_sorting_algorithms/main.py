from sorting import quick_sort, merge_sort, heap_sort, counting_sort, hybrid_sort
import numpy as np
import time
import matplotlib.pyplot as plt
from prettytable import PrettyTable


def generate_arrays(length):
    return {
        "sorted": np.arange(length),
        "reverse sorted": np.arange(length, 0, -1),
        "almost sorted": np.array(
            [i if np.random.rand() > 0.03 else length - i for i in range(length)]
        ),
        "random": np.random.randint(0, length, size=length),
        "few unique values": np.random.choice(range(10), size=length),
    }


def benchmark_algo(algo, arr):
    arr_copy = np.copy(arr)
    start_time = time.process_time()
    algo(arr_copy)
    end_time = time.process_time()
    return end_time - start_time


def run_benchmarks(algorithms, lengths, array_types):
    results = {algo.__name__: {atype: [] for atype in array_types} for algo in algorithms}
    for size in lengths:
        arrays = generate_arrays(size)
        for atype, arr in arrays.items():
            for algo in algorithms:
                time_taken = benchmark_algo(algo, arr)
                results[algo.__name__][atype].append(time_taken)
    return results


def plot_results(results, sizes, array_types):
    for algo, data in results.items():
        plt.figure(figsize=(10, 6))
        for atype in array_types:
            plt.plot(sizes, data[atype], label=atype)
        plt.title(f"Performance of {algo}")
        plt.xlabel("Array Size")
        plt.ylabel("Time (seconds)")
        plt.legend()
        plt.grid(True)
        plt.show()

    for atype in array_types:
        plt.figure(figsize=(10, 6))
        for algo, data in results.items():
            plt.plot(sizes, data[atype], label=algo)
        plt.title(f"Performance Comparison for {atype} arrays")
        plt.xlabel("Array Size")
        plt.ylabel("Time (seconds)")
        plt.legend()
        plt.grid(True)
        plt.show()


def display_avg_results(results, sizes, array_types):
    table = PrettyTable()
    table.field_names = ["Algorithm"] + [f"Size={s}" for s in sizes]

    plt.figure(figsize=(10, 6))
    for algo, data in results.items():
        avgs = []
        for size_idx, size in enumerate(sizes):
            times_for_size = []
            for atype in array_types:
                times_for_size.append(data[atype][size_idx])
            avg_time = np.mean(times_for_size)
            avgs.append(avg_time)

        plt.plot(sizes, avgs, label=algo)
        row = [algo] + [f"{t:.6f}" for t in avgs]
        table.add_row(row)

    plt.title(f"Average Performance Comparison")
    plt.xlabel("Array Size")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.show()

    print(table)


def main():
    algorithms = [quick_sort, merge_sort, heap_sort, counting_sort, hybrid_sort]
    sizes = [100, 1000, 5000, 10000, 20000, 40000, 60000, 100000]
    array_types = ["sorted", "reverse sorted", "almost sorted", "random", "few unique values"]
    results = run_benchmarks(algorithms, sizes, array_types)
    plot_results(results, sizes, array_types)
    display_avg_results(results, sizes, array_types)


if __name__ == "__main__":
    main()

# TODO: generate arrays based on type and size
#       run benchmark for single array
#       charts:
#            for each sorting method, all types of arrays
#            final:
#               for each type of array all sorting methods




