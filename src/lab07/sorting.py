def bubble_sort(nums: list[int]) -> list[int]:
    """Новый список, отсортированный по возрастанию. Исходный не меняется.

    За каждый проход самый большой элемент «всплывает» в конец. Если за
    проход не было ни одного обмена, список уже отсортирован, и мы выходим.

    bubble_sort([3, 1, 2]) -> [1, 2, 3]
    bubble_sort([2, 2, 1]) -> [1, 2, 2]
    bubble_sort([]) -> []
    """
    nums = list(nums)  # копия, иначе испортим список вызывающего
    n = len(nums)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):  # хвост из i элементов уже на местах
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:
            break
    return nums


def insertion_sort(nums: list[int]) -> list[int]:
    """Тот же контракт, что у bubble_sort.

    Берём очередной элемент и сдвигаем его влево, пока он не встанет на
    место. На почти отсортированных данных работает почти за O(n).
    """
    nums = list(nums)
    for i in range(1, len(nums)):
        key = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > key:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = key
    return nums


def selection_sort(nums: list[int]) -> list[int]:
    """Тот же контракт, что у bubble_sort.

    На каждом шаге находим минимум оставшейся части и ставим его на место.
    Всегда n^2/2 сравнений, даже на отсортированных данных.
    """
    nums = list(nums)
    n = len(nums)
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            if nums[j] < nums[smallest]:
                smallest = j
        nums[i], nums[smallest] = nums[smallest], nums[i]
    return nums


def merge_sort(nums: list[int]) -> list[int]:
    """Сортировка слиянием без рекурсии, снизу вверх, O(n log n).

    Сливаем пары соседних отрезков длины 1, потом 2, 4, 8 и так далее,
    пока отрезок не покроет весь список. Новый список, исходный не меняется.

    merge_sort([5, 2, 4, 1]) -> [1, 2, 4, 5]
    """
    a = list(nums)
    n = len(a)
    width = 1
    while width < n:
        merged = []
        for lo in range(0, n, 2 * width):
            mid = lo + width if lo + width < n else n
            hi = lo + 2 * width if lo + 2 * width < n else n
            i, j = lo, mid
            while i < mid and j < hi:
                if a[i] <= a[j]:  # <= сохраняет порядок равных элементов
                    merged.append(a[i])
                    i += 1
                else:
                    merged.append(a[j])
                    j += 1
            merged.extend(a[i:mid])
            merged.extend(a[j:hi])
        a = merged
        width *= 2
    return a


def counting_sort(nums: list[int], lo: int, hi: int) -> list[int]:
    """Сортировка подсчётом для целых в диапазоне lo..hi включительно, O(n + k).

    k = hi - lo + 1 — размер диапазона. Выгодна, когда диапазон мал по
    сравнению с n. Значение вне диапазона — ValueError.

    counting_sort([3, 1, 3, 0], 0, 3) -> [0, 1, 3, 3]
    """
    counts = [0] * (hi - lo + 1)
    for x in nums:
        if not lo <= x <= hi:
            raise ValueError(f"{x} вне диапазона {lo}..{hi}")
        counts[x - lo] += 1
    result: list[int] = []
    for offset, c in enumerate(counts):
        result.extend([lo + offset] * c)
    return result
