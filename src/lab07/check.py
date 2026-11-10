import random

from src.lab07.search import (binary_search, linear_search, two_sum_brute,
                              two_sum_fast)
from src.lab07.sorting import (bubble_sort, counting_sort, insertion_sort,
                               merge_sort, selection_sort)

checks = 0  # сколько проверок прошло; печатается в конце
# пустой, один элемент, повторы, отрицательные — их случайность может не выдать
EDGE = [[], [5], [2, 1], [1, 1, 1], [3, 1, 2], [-1, -1, 0, 5, -3]]


def counting_sort_100(nums: list[int]) -> list[int]:
    """counting_sort с диапазоном -100..100, чтобы подходил под check_sorting."""
    return counting_sort(nums, -100, 100)


def check_sorting(fn, trials: int = 100) -> None:
    """Сравнивает fn(nums) со sorted(nums) на граничных и случайных списках.

    Списки длиной 0..50, значения -100..100, с повторами. Проверяет и то,
    что исходный список не изменён. При расхождении — AssertionError с данными.
    """
    global checks
    cases = EDGE + [
        [random.randint(-100, 100) for _ in range(random.randint(0, 50))]
        for _ in range(trials)
    ]
    for nums in cases:
        original = list(nums)
        result = fn(nums)
        assert result == sorted(nums), f"{fn.__name__} ошиблась на {original}: {result}"
        assert nums == original, f"{fn.__name__} изменила исходный список {original}"
        checks += 1


def check_search(trials: int = 100) -> None:
    """linear_search против list.index, binary_search против членства в списке.

    Бинарный поиск проверяется на отсортированных списках, на отсутствующем x
    и на крайних элементах. При расхождении — AssertionError с данными.
    """
    global checks
    for _ in range(trials):
        nums = [random.randint(-20, 20) for _ in range(random.randint(0, 30))]
        x = random.randint(-25, 25)

        try:
            expected = nums.index(x)
        except ValueError:  # у list.index «нет» — исключение, у нас -1
            expected = -1
        got = linear_search(nums, x)
        assert got == expected, f"linear_search({nums}, {x}) = {got}, ожидалось {expected}"

        s = sorted(nums)
        for y in [x] + ([s[0], s[-1]] if s else []):
            got = binary_search(s, y)
            if y in s:  # индекс любого вхождения, поэтому смотрим на значение
                assert got != -1 and s[got] == y, f"binary_search({s}, {y}) = {got}"
            else:
                assert got == -1, f"binary_search({s}, {y}) = {got}, ожидалось -1"
        checks += 1


def check_two_sum(trials: int = 100) -> None:
    """Оба two_sum: либо оба None, либо оба дают пару с нужной суммой.

    Пары могут различаться (допустим любой ответ), поэтому сравнивается
    не сама пара, а её корректность. При расхождении — AssertionError.
    """
    global checks
    for _ in range(trials):
        nums = [random.randint(-50, 50) for _ in range(random.randint(0, 30))]
        target = random.randint(-100, 100)
        brute, fast = two_sum_brute(nums, target), two_sum_fast(nums, target)
        assert (brute is None) == (fast is None), (
            f"разошлись на {nums}, target={target}: brute={brute}, fast={fast}")
        for pair in (brute, fast):
            if pair is not None:
                i, j = pair
                assert i < j and nums[i] + nums[j] == target, (
                    f"неверная пара {pair} на {nums}, target={target}")
        checks += 1


if __name__ == "__main__":
    random.seed(42)
    for fn in (bubble_sort, insertion_sort, selection_sort, merge_sort,
               counting_sort_100):
        check_sorting(fn)
    check_search()
    check_two_sum()
    print(f"OK: {checks} проверок")
