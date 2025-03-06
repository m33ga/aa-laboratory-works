import numpy as np
from .quick_sort import quick_sort, insertion_sort


def hybrid_sort(arr):
    def merge(left, right, left_len, right_len):
        # Allocate temporary space proportional to the smaller run
        temp = np.empty(min(left_len, right_len), dtype=arr.dtype)

        # Binary search to find the shrinking boundaries
        left_end = left + left_len
        right_end = right + right_len

        if left_len <= right_len:
            # Copy left run to temp
            temp[:] = arr[left:left + left_len]
            i, j, k = 0, right, left  # i: temp, j: right run, k: destination
            while i < left_len and j < right_end:
                if temp[i] <= arr[j]:
                    arr[k] = temp[i]
                    i += 1
                else:
                    arr[k] = arr[j]
                    j += 1
                k += 1

            # Copy any remaining elements from temp (left run)
            remaining = left_len - i
            if remaining > 0:
                arr[k:k + remaining] = temp[i:i + remaining]
        else:
            # Copy right run to temp
            temp[:] = arr[right:right + right_len]
            i, j, k = left + left_len - 1, right_len - 1, right + right_len - 1
            while j >= 0 and i >= left:
                if temp[j] >= arr[i]:
                    arr[k] = temp[j]
                    j -= 1
                else:
                    arr[k] = arr[i]
                    i -= 1
                k -= 1

            # Copy any remaining elements from temp (right run)
            remaining = j + 1  # Number of remaining elements in temp
            if remaining > 0:
                arr[k - remaining + 1:k + 1] = temp[:remaining]

    def collapse_stack():
        while len(run_stack) > 1:
            n = len(run_stack) - 1
            if n > 1 and run_stack[n - 2][1] - run_stack[n - 2][0] <= \
               (run_stack[n][1] - run_stack[n][0]) + (run_stack[n - 1][1] - run_stack[n - 1][0]):
                if run_stack[n - 1][1] - run_stack[n - 1][0] < run_stack[n - 2][1] - run_stack[n - 2][0]:
                    n -= 1
                merge_runs(n - 1, n)
            elif run_stack[n - 1][1] - run_stack[n - 1][0] <= run_stack[n][1] - run_stack[n][0]:
                merge_runs(n - 1, n)
            else:
                break

    def merge_runs(i, j):
        left = run_stack[i][0]
        left_len = run_stack[i][1] - run_stack[i][0]
        right = run_stack[j][0]
        right_len = run_stack[j][1] - run_stack[j][0]
        merge(left, right, left_len, right_len)
        run_stack[i] = (run_stack[i][0], run_stack[j][1])
        del run_stack[j]

    def find_minrun(n):
        r = 0
        while n >= 64:
            r |= n & 1
            n >>= 1
        return n + r

    def count_unique_elements(arr):
        return len(np.unique(arr))

    # Check if counting sort is applicable
    if len(arr) > 1000 and count_unique_elements(arr) / len(arr) < 0.1:
        return counting_sort_hash(arr)

    n = len(arr)
    minrun = find_minrun(n)
    run_stack = []

    i = 0
    while i < n:
        # Find the next run
        start = i
        if i + 1 == n or arr[i] <= arr[i + 1]:
            # Ascending run
            while i + 1 < n and arr[i] <= arr[i + 1]:
                i += 1
        else:
            # Descending run
            while i + 1 < n and arr[i] > arr[i + 1]:
                i += 1
            arr[start:i + 1] = arr[start:i + 1][::-1]  # Reverse descending run

        end = i
        run_length = end - start + 1

        # Extend short runs with insertion sort
        if run_length < minrun:
            insertion_sort(arr, start, min(start + minrun - 1, n - 1))
            end = start + min(minrun - 1, n - start - 1)
            run_length = end - start + 1

        # Push the run onto the stack
        run_stack.append((start, end + 1))
        collapse_stack()

        i = end + 1

    # Merge all remaining runs
    while len(run_stack) > 1:
        merge_runs(len(run_stack) - 2, len(run_stack) - 1)

    return arr


def counting_sort_hash(arr, sorter=quick_sort):
    count = {}
    for num in arr:
        count[num] = count.get(num, 0) + 1

    unique_keys = np.array(list(count.keys()))
    sorted_keys = sorter(unique_keys)

    sorted_arr = []
    for key in sorted_keys:
        sorted_arr.extend([key] * count[key])

    return np.array(sorted_arr)