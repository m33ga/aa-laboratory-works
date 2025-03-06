import numpy as np


def merge_sort(arr):
    def merge(left, right):
        result = np.empty(len(left) + len(right), dtype=arr.dtype)
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result[k] = left[i]
                i += 1
            else:
                result[k] = right[j]
                j += 1
            k += 1
        result[k:] = left[i:] if i < len(left) else right[j:]
        return result

    def _merge_sort(arr):
        if len(arr) <= 10:
            return insertion_sort(arr)
        mid = len(arr) // 2
        left = _merge_sort(arr[:mid])
        right = _merge_sort(arr[mid:])
        return merge(left, right)

    return _merge_sort(arr)


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

