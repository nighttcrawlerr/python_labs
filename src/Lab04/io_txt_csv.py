import csv
from pathlib import Path
from typing import Iterable, Sequence


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Читает текстовый файл целиком и возвращает его содержимым одной строкой.

    По умолчанию файл читается в UTF-8. Чтобы прочитать файл в другой
    кодировке, передайте её явно, например: read_text(path, encoding="cp1251").

    Исключения намеренно не перехватываются — вызывающий код сам решает,
    что делать с отсутствующим файлом или неподходящей кодировкой.

    Args:
        path: путь к файлу — строка или Path.
        encoding: кодировка файла, по умолчанию "utf-8".

    Returns:
        Содержимое файла одной строкой. Для пустого файла — пустая строка.

    Raises:
        FileNotFoundError: если файла по указанному пути нет.
        IsADirectoryError: если путь указывает на директорию, а не файл.
        UnicodeDecodeError: если файл не читается в указанной кодировке.
    """
    p = Path(path)
    return p.read_text(encoding=encoding)


def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    """Записывает строки в CSV-файл с разделителем «запятая».

    Существующий файл перезаписывается. Запись идёт через csv.writer,
    поэтому значения с запятыми и кавычками экранируются автоматически.

    Пустой rows без header создаёт пустой файл, с header — файл только
    с заголовком.

    Args:
        rows: строки таблицы; все должны быть одинаковой длины.
        path: путь к создаваемому файлу — строка или Path.
        header: заголовок таблицы; если None, заголовок не пишется.

    Returns:
        None.

    Raises:
        TypeError: если строка таблицы не список и не кортеж.
        ValueError: если строки в rows разной длины.
    """
    p = Path(path)
    rows = list(rows)
    # проверяем до открытия файла, чтобы не оставить битый csv
    for row in rows:
        # строка тоже имеет len и развалилась бы на буквы по колонкам
        if not isinstance(row, (list, tuple)):
            raise TypeError(
                f"Строка таблицы должна быть списком или кортежем, "
                f"получен {type(row).__name__}."
            )
    lengths = {len(row) for row in rows}
    if len(lengths) > 1:
        raise ValueError("Все строки должны быть одной длины")
    # newline="" обязателен для csv, иначе на Windows лишние пустые строки
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if header is not None:
            w.writerow(header)
        for r in rows:
            w.writerow(r)


def ensure_parent_dir(path: str | Path) -> None:
    """Создаёт директорию, в которой должен лежать указанный файл.

    Нужна перед записью в файл, если папки может ещё не существовать.
    Промежуточные директории создаются тоже, а уже существующая папка
    ошибкой не считается.

    Args:
        path: путь к файлу (не к папке) — строка или Path.

    Returns:
        None.
    """
    p = Path(path)
    # exist_ok, чтобы второй запуск не падал на уже созданной папке
    p.parent.mkdir(parents=True, exist_ok=True)
    