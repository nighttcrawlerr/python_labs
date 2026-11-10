def linear_search(nums: list[int], x: int) -> int:
    """Индекс первого вхождения x или -1.

    linear_search([4, 2, 7, 2], 2) -> 1
    linear_search([4, 2, 7, 2], 9) -> -1
    linear_search([], 1) -> -1
    """
    for i, value in enumerate(nums):
        if value == x:
            return i
    return -1


def binary_search(sorted_nums: list[int], x: int) -> int:
    """Индекс x в отсортированном по возрастанию списке или -1.

    Список должен быть уже отсортирован. На неотсортированном списке
    результат не определён: функция может вернуть -1 для числа, которое
    в списке есть. Если x встречается несколько раз, вернётся индекс любого
    из вхождений.

    binary_search([1, 3, 5, 7], 5) -> 2
    binary_search([1, 3, 5, 7], 4) -> -1
    binary_search([5], 5) -> 0
    binary_search([], 5) -> -1
    """
    lo, hi = 0, len(sorted_nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_nums[mid] == x:
            return mid
        if sorted_nums[mid] < x:
            lo = mid + 1  # x может быть только правее
        else:
            hi = mid - 1  # x может быть только левее
    return -1


def two_sum_brute(nums: list[int], target: int) -> tuple[int, int] | None:
    """Пара индексов (i, j), i < j, nums[i] + nums[j] == target, или None.

    Перебор всех пар, два вложенных цикла, O(n^2).

    two_sum_brute([2, 7, 11, 15], 9) -> (0, 1)
    two_sum_brute([1, 2], 10) -> None
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum_fast(nums: list[int], target: int) -> tuple[int, int] | None:
    """То же, что two_sum_brute, но за один проход со словарём, O(n).

    Словарь хранит «значение -> индекс». Для каждого x смотрим, не встречали
    ли мы уже target - x. При нескольких подходящих парах вернётся любая.

    two_sum_fast([2, 7, 11, 15], 9) -> (0, 1)
    two_sum_fast([3, 3], 6) -> (0, 1)
    """
    seen: dict[int, int] = {}
    for j, x in enumerate(nums):
        if target - x in seen:
            return (seen[target - x], j)
        # кладём после проверки, иначе элемент спарится сам с собой
        seen[x] = j
    return None
