import matplotlib.pyplot as plt
import time
import timeit
import math
from decimal import Context, Decimal, ROUND_HALF_EVEN
import sys


def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_memo_recursive(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 2:
        return 1
    if n not in memo:
        memo[n] = fib_memo_recursive(n - 1, memo) + fib_memo_recursive(n - 2, memo)
    return memo[n]


def fib_iterative(n):
    f_0, f_1 = 0, 1
    for i in range(n):
        f_0, f_1 = f_1, f_0 + f_1
    return f_0


def fib_memo(n):
    memo = [0, 1]
    for i in range(2, n + 1):
        memo.append(memo[i - 1] + memo[i - 2])
    return memo[n]


def fib_matrix(n):
    F = [[1, 1],
         [1, 0]]
    if n == 0:
        return 0
    power(F, n - 1)

    return F[0][0]


def multiply(F, M):
    x = (F[0][0] * M[0][0] +
         F[0][1] * M[1][0])
    y = (F[0][0] * M[0][1] +
         F[0][1] * M[1][1])
    z = (F[1][0] * M[0][0] +
         F[1][1] * M[1][0])
    w = (F[1][0] * M[0][1] +
         F[1][1] * M[1][1])

    F[0][0] = x
    F[0][1] = y
    F[1][0] = z
    F[1][1] = w


def power(F, n):
    if n == 0 or n == 1:
        return
    M = [[1, 1],
         [1, 0]]

    power(F, n // 2)
    multiply(F, F)

    if n % 2 != 0:
        multiply(F, M)


def fib_binet(n):
    ctx = Context(prec=60, rounding=ROUND_HALF_EVEN)
    sqrt_5 = Decimal(5).sqrt()
    phi = (1 + sqrt_5) / 2
    psi = (1 - sqrt_5) / 2

    return int((ctx.power(phi, Decimal(n)) - ctx.power(psi, Decimal(n))) / sqrt_5)


def fib_fast_doubling_main(n):
    return fib_fast_doubling(n)[0]


def fib_fast_doubling(n):
    if n == 0:
        return 0, 1
    a, b = fib_fast_doubling(n // 2)
    c = a * (b * 2 - a)
    d = a * a + b * b
    if n % 2 == 0:
        return c, d
    return d, c + d


def measure_time(func, terms):
    times = []
    for n in terms:
        start = time.process_time()
        func(n)
        end = time.process_time()
        times.append(end - start)
        # times.append(timeit.timeit(lambda: func(n), number=1))
    return times


def main():
    terms_list_short = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45]
    # terms_list_long = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
    terms_list_long = [
        501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981,
        5012, 6310, 7943, 10000, 12589, 15849, 19953, 25118, 31623,
        39810, 50118, 63096, 79433, 100000, 125892
    ]

    algorithms = [
        # ("Recursive", fib_recursive, terms_list_short),
        # ("Recursive Memo", fib_memo_recursive, terms_list_short),
        ("Iterative", fib_iterative, terms_list_long),
        ("DP Memoization", fib_memo, terms_list_long),
        ("Matrix Fast Exponentiation", fib_matrix, terms_list_long),
        ("Binet", fib_binet, terms_list_long),
        ("Fast Doubling", fib_fast_doubling_main, terms_list_long)
    ]

    results = {}
    for name, func, terms in algorithms:
        results[name] = measure_time(func, terms)
        print(results[name])

    for name, times in results.items():
        plt.figure(figsize=(10, 6))
        plt.plot(terms_list_long if "Recursive" not in name else terms_list_short, times, marker='o', linestyle='-')
        plt.xlabel("Fibonacci Term")
        plt.ylabel("Execution Time (s)")
        plt.title(f"{name} Execution Time")
        plt.grid(True)
        plt.show()

    plt.figure(figsize=(10, 6))
    for name, times in results.items():
        if "Recursive" not in name:
            plt.plot(terms_list_long, times, label=name, marker='o')
        # if "Fast" in name:
        #     plt.plot(terms_list_long, times, label=name, marker='o')

    plt.xlabel("Fibonacci Term")
    plt.ylabel("Execution Time (s)")
    plt.title("Fibonacci Algorithms Execution Time Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    for name, times in results.items():
        if "Recursive" in name:
            plt.plot(terms_list_short, times, label=name, marker='o')

    plt.xlabel("Fibonacci Term")
    plt.ylabel("Execution Time (s)")
    plt.title("Recursive Fibonacci Algorithms Execution Time Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
