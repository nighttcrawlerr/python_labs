import csv
import json


def json_to_csv(json_path: str, csv_path: str) -> None:
    """Преобразует JSON-файл со списком словарей в CSV.

    Колонки — объединение ключей всех объектов. Порядок колонок:
    как в первом объекте, новые ключи добавляются в конец по мере
    появления. Если у объекта какого-то поля нет, в ячейку пишется
    пустая строка.

    Кодировка на чтении и записи — строго UTF-8.

    Args:
        json_path: путь к входному JSON (список словарей).
        csv_path: путь к создаваемому CSV; существующий перезаписывается.

    Returns:
        None.

    Raises:
        FileNotFoundError: если входного файла нет.
        ValueError: если JSON не список, список пуст или его элемент
            не словарь.
    """
    # load — из файла; loads — из строки
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # ждём именно список объектов, а не один объект и не список чисел
    if not isinstance(data, list):
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    if not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    # собираем объединение ключей; set не подходит — он теряет порядок
    fieldnames = []
    for obj in data:
        if not isinstance(obj, dict):
            raise ValueError("Пустой JSON или неподдерживаемая структура")
        for key in obj:
            if key not in fieldnames:
                fieldnames.append(key)

    # newline="" обязателен для csv, иначе на Windows лишние пустые строки
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        # restval подставится там, где у объекта ключа нет (напр. city у Веры)
        w = csv.DictWriter(f, fieldnames=fieldnames, restval="")
        w.writeheader()
        w.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    """Преобразует CSV в JSON — список словарей, по словарю на строку.

    Первая строка CSV считается заголовком и даёт ключи. Все значения
    остаются строками: CSV не хранит типы, поэтому число 22 вернётся
    как "22". Из-за этого цепочка JSON → CSV → JSON не восстанавливает
    исходные типы.

    CSV, в котором есть только заголовок и нет строк данных, ошибкой
    не считается — результатом будет пустой список.

    Кодировка на чтении и записи — строго UTF-8.

    Args:
        csv_path: путь к входному CSV с заголовком.
        json_path: путь к создаваемому JSON; существующий перезаписывается.

    Returns:
        None.

    Raises:
        FileNotFoundError: если входного файла нет.
        ValueError: если в файле нет заголовка (файл пуст).
    """
    with open(csv_path, newline="", encoding="utf-8") as f:
        # DictReader берёт первую строку как имена ключей
        reader = csv.DictReader(f)
        rows = list(reader)
        # у совсем пустого файла заголовка нет — fieldnames остаётся None
        if reader.fieldnames is None:
            raise ValueError("CSV без заголовка или пустой")

    with open(json_path, "w", encoding="utf-8") as f:
        # ensure_ascii=False — кириллица, а не \uXXXX; indent=2 — отступы
        json.dump(rows, f, ensure_ascii=False, indent=2)



def _show(path: str) -> None:
    """Печатает содержимое файла — для демонстрации в консоли."""
    print(f"--- {path}")
    with open(path, encoding="utf-8") as f:
        print(f.read().rstrip())


if __name__ == "__main__":
    # пути относительные, запускать из корня проекта
    print("=" * 52)
    print("JSON -> CSV")
    print("=" * 52)
    _show("data/samples/people.json")
    json_to_csv("data/samples/people.json", "data/out/people_from_json.csv")
    _show("data/out/people_from_json.csv")

    with open("data/out/people_from_json.csv", encoding="utf-8") as f:
        lines = f.read().splitlines()
    print(f"проверка: заголовок {lines[0]!r}, строк данных {len(lines) - 1}")
    print("у Веры нет города -> последняя ячейка пустая")

    print()
    print("=" * 52)
    print("CSV -> JSON")
    print("=" * 52)
    _show("data/samples/people.csv")
    csv_to_json("data/samples/people.csv", "data/out/people_from_csv.json")
    _show("data/out/people_from_csv.json")

    with open("data/out/people_from_csv.json", encoding="utf-8") as f:
        objs = json.load(f)
    print(f"проверка: ключи {list(objs[0])}, объектов {len(objs)}")
    print('значения строками: age = "22", а не 22')
