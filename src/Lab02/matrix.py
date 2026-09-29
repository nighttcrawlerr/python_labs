def _check_rect(mat: list[list[float | int]]) -> None:
    """Проверка на рваную матрицу
    
    Args:
        mat: Матрица(список списков)

    Returns:
        None
    
    Raises:
        ValueError: Если строки разной длины
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

def row_sums(mat):
    _check_rect(mat)
    return [sum(row) for row in mat]

def col_sums(mat):
    return row_sums(transpose(mat))