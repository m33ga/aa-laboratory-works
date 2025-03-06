import numpy as np


def counting_sort(arr):
    min_val = np.min(arr)
    max_val = np.max(arr)
    count = np.zeros(max_val - min_val + 1, dtype=int)
    for num in arr:
        count[num - min_val] += 1
    sorted_arr = np.repeat(np.arange(min_val, max_val + 1), count)
    return sorted_arr

