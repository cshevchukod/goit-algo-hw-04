#Запуск: python main.py

from random import randint, seed
from timeit import repeat


# ---------- 1) Insertion sort ----------

def insertion_sort(arr):
    a = arr[:]  # копія, щоб не псувати оригінал
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# ---------- 2) Merge sort ----------

def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]  # повертаємо копію

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# ---------- 3) TimSort (built-in) ----------

def timsort(arr):
    return sorted(arr)


# ---------- Data sets ----------

def data_random(n):
    return [randint(0, 100_000) for _ in range(n)]

def data_sorted(n):
    return list(range(n))

def data_reversed(n):
    return list(range(n, 0, -1))

def data_almost_sorted(n):
    # майже відсортований: кілька випадкових swap
    a = list(range(n))
    swaps = max(1, n // 100)  # ~1%
    for _ in range(swaps):
        i = randint(0, n - 1)
        j = randint(0, n - 1)
        a[i], a[j] = a[j], a[i]
    return a


# ---------- Benchmark ----------

def measure(func, arr, number=3, repeat_n=5):
    times = repeat(lambda: func(arr), repeat=repeat_n, number=number)
    return min(times) / number  # час одного запуску (сек)

def maintask():
    seed(42)

    algorithms = [
        ("insertion_sort", insertion_sort),
        ("merge_sort", merge_sort),
        ("timsort(sorted)", timsort),
    ]

    datasets = [
        ("random", data_random),
        ("sorted", data_sorted),
        ("reversed", data_reversed),
        ("almost_sorted", data_almost_sorted),
    ]

    sizes = [100, 500, 1000, 2000, 5000]

    for ds_name, ds_func in datasets:
        print(f"\n=== Dataset: {ds_name} ===")
        print("n\tinsertion\tmerge\ttimsort")

        for n in sizes:
            arr = ds_func(n)

            number = 1 if n >= 2000 else 3

            results = {}
            for algo_name, algo_func in algorithms:
                results[algo_name] = measure(algo_func, arr, number=number)

            print(
                f"{n}\t"
                f"{results['insertion_sort']:.8f}\t"
                f"{results['merge_sort']:.8f}\t"
                f"{results['timsort(sorted)']:.8f}"
            )


if __name__ == "__main__":
    maintask()
