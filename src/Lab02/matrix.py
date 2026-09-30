def _check_rect(mat: list[list[float | int]]) -> None:
    """Проверяет, что матрица прямоугольная (строки одной длины).

    Args:
        mat: матрица (список списков). Пустая матрица считается корректной.

    Returns:
        None. Функция либо молча завершается, либо кидает исключение.

    Raises:
        ValueError: если строки матрицы разной длины.
    """
    lengths = {len(row) for row in mat}
    if len(lengths) > 1:
        raise ValueError("Строки не могут быть разной длины")


def transpose(mat: list[list[float | int]]) -> list[list]:
    """Меняет строки и столбцы матрицы местами.

    Args:
        mat: прямоугольная матрица (список списков).

    Returns:
        Новая матрица, где строки и столбцы поменяны местами.
        Для пустой матрицы — пустой список.

    Raises:
        ValueError: если строки матрицы разной длины.
    """
    _check_rect(mat)
    if not mat:
        return []
    result = []
    for j in range(len(mat[0])):
        result.append([row[j] for row in mat])
    return result


def row_sums(mat: list[list[float | int]]) -> list[float]:
    """Считает сумму элементов каждой строки матрицы.

    Args:
        mat: прямоугольная матрица (список списков).

    Returns:
        Список сумм по строкам. Для пустой матрицы — пустой список.

    Raises:
        ValueError: если строки матрицы разной длины.
    """
    _check_rect(mat)
    return [sum(row) for row in mat]


def col_sums(mat: list[list[float | int]]) -> list[float]:
    """Считает сумму элементов каждого столбца матрицы.

    Столбцы получаются транспонированием, после чего считаются суммы
    строк — поэтому функция переиспользует transpose() и row_sums().

    Args:
        mat: прямоугольная матрица (список списков).

    Returns:
        Список сумм по столбцам. Для пустой матрицы — пустой список.

    Raises:
        ValueError: если строки матрицы разной длины.
    """
    return row_sums(transpose(mat))


if __name__ == "__main__":
    print("--- transpose ---")
    print(transpose([[1, 2, 3]]))
    print(transpose([[1], [2], [3]]))
    print(transpose([[1, 2], [3, 4]]))
    print(transpose([]))

    print("--- row_sums ---")
    print(row_sums([[1, 2, 3], [4, 5, 6]]))
    print(row_sums([[-1, 1], [10, -10]]))
    print(row_sums([[0, 0], [0, 0]]))

    print("--- col_sums ---")
    print(col_sums([[1, 2, 3], [4, 5, 6]]))
    print(col_sums([[-1, 1], [10, -10]]))
    print(col_sums([[0, 0], [0, 0]]))

    # Проверка исключения: программа намеренно падает с ValueError.
    print("--- рваная матрица ---")
    print(transpose([[1, 2], [3]]))