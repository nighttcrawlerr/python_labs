import random
import timeit

from src.Lab04.io_txt_csv import ensure_parent_dir, write_csv
from src.lab07.search import (binary_search, linear_search, two_sum_brute,
                              two_sum_fast)
from src.lab07.sorting import (bubble_sort, counting_sort, insertion_sort,
                               merge_sort, selection_sort)

CSV_PATH = "data/lab07/bench.csv"
LIMIT = 60  # секунд; квадратичную сортировку, которая заведомо дольше, не запускаем

Row = tuple[str, int, str, float | str]


def measure(fn, repeat: int = 1) -> float:
    """Лучшее из repeat запусков fn в секундах (один вызов за замер)."""
    return min(timeit.repeat(fn, number=1, repeat=repeat))


def bench_sorts() -> list[Row]:
    """Сортировки на одних и тех же данных для каждого n."""
    rows: list[Row] = []
    slow = {"bubble_sort": bubble_sort, "insertion_sort": insertion_sort,
            "selection_sort": selection_sort}
    previous: dict[str, tuple[int, float]] = {}  # impl -> (прошлый n, время)
    for n in (1_000, 10_000, 100_000):
        random.seed(42)
        data = [random.randint(0, 10**6) for _ in range(n)]
        rows.append(("sort", n, "sorted", measure(lambda: sorted(data), 3)))
        rows.append(("sort", n, "merge_sort", measure(lambda: merge_sort(data), 3)))
        for name, fn in slow.items():
            if name in previous:
                prev_n, prev_t = previous[name]
                # O(n^2): при росте n в k раз время растёт в k^2 раз
                if prev_t * (n / prev_n) ** 2 > LIMIT:
                    rows.append(("sort", n, name, f">{LIMIT}"))
                    continue
            t = measure(lambda: fn(data))
            previous[name] = (n, t)
            rows.append(("sort", n, name, t))

    # диапазон мал по сравнению с n: здесь подсчёт должен обгонять sorted
    random.seed(42)
    n = 100_000
    small = [random.randint(0, 100) for _ in range(n)]
    rows.append(("sort_range_0_100", n, "sorted", measure(lambda: sorted(small), 5)))
    rows.append(("sort_range_0_100", n, "counting_sort",
                 measure(lambda: counting_sort(small, 0, 100), 5)))
    return rows


def bench_search() -> list[Row]:
    """10 000 запросов к списку из 100 000; бинарному засчитываем и сортировку."""
    random.seed(42)
    n = 100_000
    data = [random.randint(0, 10**6) for _ in range(n)]
    queries = [random.choice(data) for _ in range(10_000)]  # все запросы найдутся

    t_linear = measure(lambda: [linear_search(data, q) for q in queries])
    t_sort = measure(lambda: sorted(data), 3)
    sorted_data = sorted(data)
    t_binary = measure(lambda: [binary_search(sorted_data, q) for q in queries], 3)
    return [
        ("search", n, "linear_search", t_linear),
        ("search", n, "sorted (подготовка)", t_sort),
        ("search", n, "binary_search", t_binary),
        ("search", n, "sorted + binary_search", t_sort + t_binary),
    ]


def bench_two_sum() -> list[Row]:
    """Two Sum в худшем для перебора случае: ответ — последняя пара."""
    rows: list[Row] = []
    for n in (1_000, 10_000):
        random.seed(42)
        nums = random.sample(range(10**9), n)  # без повторов, пара единственная
        target = nums[-2] + nums[-1]
        rows.append(("two_sum", n, "two_sum_brute",
                     measure(lambda: two_sum_brute(nums, target))))
        rows.append(("two_sum", n, "two_sum_fast",
                     measure(lambda: two_sum_fast(nums, target), 5)))
    return rows


def print_table(rows: list[Row]) -> None:
    """Печатает замеры таблицей с выровненными столбцами."""
    shown = [(task, f"{n:,}".replace(",", " "),
              impl, sec if isinstance(sec, str) else f"{sec:.6f}")
             for task, n, impl, sec in rows]
    header = ("task", "n", "impl", "seconds")
    widths = [max(len(str(r[i])) for r in shown + [header]) for i in range(4)]
    line = "  ".join(f"{h:<{w}}" for h, w in zip(header, widths))
    print(line)
    print("-" * len(line))
    for r in shown:
        print("  ".join(f"{c:>{w}}" if i in (1, 3) else f"{c:<{w}}"
                        for i, (c, w) in enumerate(zip(r, widths))))


if __name__ == "__main__":
    all_rows = bench_sorts() + bench_search() + bench_two_sum()
    print_table(all_rows)
    ensure_parent_dir(CSV_PATH)
    # фиксированный формат: round() оставил бы 3.9e-05 вместо 0.000039
    csv_rows = [(task, n, impl, sec if isinstance(sec, str) else f"{sec:.6f}")
                for task, n, impl, sec in all_rows]
    write_csv(csv_rows, CSV_PATH, header=("task", "n", "impl", "seconds"))
    print(f"\nзаписано: {CSV_PATH}")
