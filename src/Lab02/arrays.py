def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """Находит минимальное и максимальное значения в списке чисел.

    Args:
        nums: непустой список чисел (int или float).

    Returns:
        Кортеж из двух элементов: (минимум, максимум).

    Raises:
        ValueError: если список пуст.
    """
    if not nums:
        raise ValueError("Список не должен быть пустым.")

    minimum = min(nums)
    maximum = max(nums)

    return (minimum, maximum)

print(min_max([]))  