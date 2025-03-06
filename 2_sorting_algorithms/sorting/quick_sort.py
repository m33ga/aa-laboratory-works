import numpy as np


def quick_sort(arr):
    def partition_three_way(low, high):
        # random pivot turns better than median of 3
        pivot_idx = np.random.randint(low, high + 1)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]

        pivot = arr[high]
        lt = low
        gt = high
        i = low

        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[gt], arr[i] = arr[i], arr[gt]
                gt -= 1
            else:
                i += 1

        return lt, gt

    def _quick_sort_iterative(low, high):
        stack = [(low, high)]

        while stack:
            low, high = stack.pop()

            if high - low <= 10:
                insertion_sort(arr, low, high)
                continue

            if low < high:
                lt, gt = partition_three_way(low, high)

                if gt - lt < high - (gt + 1):
                    stack.append((gt + 1, high))
                    stack.append((low, lt - 1))
                else:
                    stack.append((low, lt - 1))
                    stack.append((gt + 1, high))

    _quick_sort_iterative(0, len(arr) - 1)
    return arr


def insertion_sort(arr, low, high):
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

