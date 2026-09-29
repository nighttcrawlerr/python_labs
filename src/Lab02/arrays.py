def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """Находит минимальное и максимальное значения в списке чисел.

    Оба значения ищутся за один проход по списку, вручную,
    без встроенных функций min() и max().

    Args:
        nums: непустой список чисел (int или float).

    Returns:
        Кортеж из двух элементов: (минимум, максимум).

    Raises:
        ValueError: если список пуст.
    """
    if not nums:
        raise ValueError("Список не должен быть пустым.")

    minimum = nums[0]
    maximum = nums[0]

    for num in nums:
        if num < minimum:
            minimum = num
        if num > maximum:
            maximum = num

    return (minimum, maximum)


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """Возвращает отсортированный по возрастанию список уникальных чисел.

    Дубликаты убираются через set, сортировка выполнена вручную
    методом пузырька, без встроенных sorted() и list.sort().
    Значения 1 и 1.0 считаются одним и тем же числом.

    Args:
        nums: список чисел (int или float).

    Returns:
        Новый отсортированный список уникальных чисел.
    """
    result = list(set(nums))

    for i in range(len(result)):
        for j in range(len(result) - 1 - i):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]

    return result


def flatten(mat: list[list | tuple]) -> list:
    """Преобразует список списков/кортежей в одномерный список.

    Элементы собираются построчно (row-major).

    Args:
        mat: список, каждый элемент которого — список или кортеж.

    Returns:
        Одномерный список со всеми элементами матрицы.

    Raises:
        TypeError: если элемент mat не является списком или кортежем.
    """
    result = []
    for row in mat:
        if not isinstance(row, (list, tuple)):
            raise TypeError(
                f"Каждый элемент матрицы должен быть списком или кортежем, "
                f"получен {type(row).__name__}."
            )
        result.extend(row)
    return result


if __name__ == "__main__":
    print("--- min_max ---")
    print(min_max([3, -1, 5, 5, 0]))
    print(min_max([42]))
    print(min_max([-5, -2, -9]))
    print(min_max([1.5, 2, 2.0, -3.1]))

    print("--- unique_sorted ---")
    print(unique_sorted([3, 1, 2, 1, 3]))
    print(unique_sorted([]))
    print(unique_sorted([-1, -1, 0, 2, 2]))
    print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))

    print("--- flatten ---")
    print(flatten([[1, 2], [3, 4]]))
    print(flatten([[1, 2], (3, 4, 5)]))
    print(flatten([[1], [], [2, 3]]))

    # Проверка исключения: программа намеренно падает с ValueError.
    print("--- min_max([]) ---")
    print(min_max([]))
