import csv
import json

from src.Lab04.io_txt_csv import ensure_parent_dir
from src.lab08.models import format_student, student_from_dict, student_to_dict


def students_to_json(students: list[dict], path: str) -> None:
    """Сохраняет список записей в JSON: массив объектов, UTF-8, отступ 2.

    Каждая запись проходит через student_to_dict, то есть проверяется.

    Raises:
        ValueError: если какая-то запись не проходит валидацию.
    """
    data = [student_to_dict(s) for s in students]
    ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def students_from_json(path: str) -> list[dict]:
    """Читает JSON-массив и превращает каждый объект в проверенную запись.

    Политика для битых записей — strict: первая же ошибка прерывает чтение,
    ValueError содержит номер записи (с единицы) и причину. Пропускать
    битые молча нельзя: программа не должна работать с неверными данными.

    Raises:
        FileNotFoundError: если файла нет.
        ValueError: если JSON сломан, это не массив или запись не прошла проверку.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)  # битый JSON даст JSONDecodeError, это подкласс ValueError
    if not isinstance(data, list):
        raise ValueError("JSON должен быть массивом записей")
    students = []
    for i, d in enumerate(data, 1):
        try:
            students.append(student_from_dict(d))
        except ValueError as e:
            raise ValueError(f"запись {i}: {e}") from e
    return students


def students_from_csv(path: str) -> list[dict]:
    """★ Читает записи из CSV с заголовком fio,birthdate,group,gpa. Политика strict.

    Из CSV gpa приходит строкой, поэтому приводится к float здесь, на входе,
    один раз; student_from_dict строку в gpa не принимает.

    Raises:
        FileNotFoundError: если файла нет.
        ValueError: если запись не прошла проверку (в сообщении номер записи).
    """
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    students = []
    for i, row in enumerate(rows, 1):
        try:
            try:
                row["gpa"] = float(row["gpa"])
            except (KeyError, TypeError, ValueError):
                raise ValueError(f"gpa: {row.get('gpa')!r} не число") from None
            students.append(student_from_dict(row))
        except ValueError as e:
            raise ValueError(f"запись {i}: {e}") from e
    return students


if __name__ == "__main__":
    # пути относительные, запускать из корня проекта
    src = "data/lab08/students_input.json"
    out = "data/lab08/students_output.json"
    bad = "data/lab08/students_bad.json"

    print("--- корректные записи туда-обратно ---")
    students = students_from_json(src)
    for s in students:
        print(" ", format_student(s))
    students_to_json(students, out)
    print(f"записано: {out}")
    print("прочитано обратно, совпадает:", students_from_json(out) == students)

    print(f"\n--- битые записи ({bad}) ---")
    with open(bad, encoding="utf-8") as f:
        for i, d in enumerate(json.load(f), 1):
            try:
                student_from_dict(d)
                print(f"  запись {i}: ок")
            except ValueError as e:
                print(f"  запись {i}: {e}")
    try:
        students_from_json(bad)
    except ValueError as e:
        print(f"students_from_json (strict): {e}")
