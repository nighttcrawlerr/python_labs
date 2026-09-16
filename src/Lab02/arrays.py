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

def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """Возвращает отсортированный список уникальных чисел.

    Args:
        nums: список чисел (int или float).

    Returns:
        Отсортированный список уникальных чисел.
    """
    return sorted(set(nums))

print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))

def flatten(mat: list[list | tuple]) -> list:
    """Преобразует двумерный список или кортеж в одномерный список.

    Args:
        mat: двумерный список или кортеж.

    Returns:
        Одномерный список, содержащий все элементы из матрицы.
    """
    return [item for sublist in mat for item in sublist]