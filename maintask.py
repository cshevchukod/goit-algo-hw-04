#Запуск: python main.py

from random import randint, seed
from timeit import repeat

def insertion_sort(arr):
    # Сортування вставками (повертає новий список, оригінал не змінює)
    a = arr[:]  # копія
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr):
    # Сортування злиттям (ділимо список навпіл, сортуємо частини, зливаємо)
    if len(arr) <= 1:
        return arr[:]  # копія
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    # Злиття двох вже відсортованих списків у один відсортований
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

def timsort(arr):
    # TimSort у Python (вбудована функція sorted)
    return sorted(arr)

# ---------- Генерація тестових даних ----------

def make_random(n):
    # випадкові числа
    return [randint(0, 100_000) for _ in range(n)]

def make_sorted(n):
    # вже відсортований список
    return list(range(n))

def make_reversed(n):
    # відсортований у зворотньому порядку
    return list(range(n, 0, -1))

def make_almost_sorted(n):
    # майже відсортований: робимо ~1% випадкових перестановок
    a = list(range(n))
    swaps = max(1, n // 100)
    for _ in range(swaps):
        i = randint(0, n - 1)
        j = randint(0, n - 1)
        a[i], a[j] = a[j], a[i]
    return a

# ---------- Вимірювання часу ----------

def measure(func, arr, number=3, repeat_n=5):
    times = repeat(lambda: func(arr), repeat=repeat_n, number=number)
    return min(times) / number


def main():
    seed(42)  # щоб random-дані були стабільні при кожному запуску

    sizes = [100, 500, 1000, 2000, 5000]

    # Кожен датасет: (назва, функція-генератор)
    for ds_name, ds_fn in [
        ("random", make_random),
        ("sorted", make_sorted),
        ("reversed", make_reversed),
        ("almost_sorted", make_almost_sorted),
    ]:
        print(f"\n=== {ds_name} ===")
        print("n\tinsertion\tmerge\ttimsort")

        for n in sizes:
            arr = ds_fn(n)

            # на великих n робимо менше повторів, щоб не чекати дуже довго
            number = 1 if n >= 2000 else 3

            t_ins = measure(insertion_sort, arr, number=number)
            t_mrg = measure(merge_sort, arr, number=number)
            t_tim = measure(timsort, arr, number=number)

            print(f"{n}\t{t_ins:.8f}\t{t_mrg:.8f}\t{t_tim:.8f}")

if __name__ == "__main__":
    main()
