from datetime import date

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")


def _check_values(fio, birthdate, group, gpa) -> None:
    """Проверяет значения четырёх полей; первая же ошибка — ValueError.

    Общие правила для make_student и validate_student лежат в одном месте.
    В сообщении всегда видно, какое поле и почему не подошло.
    """
    for name, value in (("fio", fio), ("group", group)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name}: нужна непустая строка, получено {value!r}")

    try:
        born = date.fromisoformat(birthdate)
        # fromisoformat принимает и "20030215", а по заданию нужен YYYY-MM-DD
        ok = born.isoformat() == birthdate
    except (TypeError, ValueError):  # 2003-02-30 даёт ValueError, не-строка — TypeError
        ok = False
    if not ok:
        raise ValueError(f"birthdate: {birthdate!r} не дата в формате YYYY-MM-DD")
    if born > date.today():
        raise ValueError(f"birthdate: {birthdate} в будущем")

    # bool — подкласс int, поэтому True иначе прошёл бы как gpa = 1
    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise ValueError(f"gpa: нужно число, получено {gpa!r}")
    if not 0 <= gpa <= 5:
        raise ValueError(f"gpa: {gpa} вне диапазона 0..5")


def make_student(fio: str, birthdate: str, group: str, gpa: float) -> dict:
    """Собирает запись Student, проверив каждое поле.

    fio и group очищаются от пробелов по краям, int в gpa приводится к float.

    make_student("Иванов Иван Иванович", "2007-05-14", "БИВТ-26-6-1", 4.3)
    -> {"fio": ..., "birthdate": "2007-05-14", "group": ..., "gpa": 4.3}

    Raises:
        ValueError: если какое-то поле не подошло (в сообщении имя поля).
    """
    _check_values(fio, birthdate, group, gpa)
    return {"fio": fio.strip(), "birthdate": birthdate,
            "group": group.strip(), "gpa": float(gpa)}


def validate_student(rec: dict) -> None:
    """Проверяет готовую запись: набор ключей ровно STUDENT_FIELDS и значения.

    Ничего не возвращает и запись не меняет.

    Raises:
        ValueError: если это не словарь, ключи не совпадают с STUDENT_FIELDS
            или значение какого-то поля не подошло.
    """
    if not isinstance(rec, dict):
        raise ValueError(f"запись должна быть словарём, получено {type(rec).__name__}")
    if set(rec) != set(STUDENT_FIELDS):
        missing = sorted(set(STUDENT_FIELDS) - set(rec))
        extra = sorted(map(str, set(rec) - set(STUDENT_FIELDS)))
        raise ValueError(f"ключи записи не совпадают с STUDENT_FIELDS: "
                         f"нет {missing}, лишние {extra}")
    _check_values(rec["fio"], rec["birthdate"], rec["group"], rec["gpa"])


def student_age(rec: dict, today: date | None = None) -> int:
    """Полных лет на дату today (по умолчанию сегодня).

    Родившийся 2007-09-20 на 2026-09-19 ещё не отметил день рождения: 18 лет.
    """
    born = date.fromisoformat(rec["birthdate"])
    today = today or date.today()
    # кортеж (месяц, день) сравнивается как пара: был ли день рождения в этом году
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def _years(n: int) -> str:
    """Склонение: 1 год, 2-4 года, 5-20 лет, 21 год, 22 года, 111 лет."""
    if 11 <= n % 100 <= 14:
        return "лет"
    return {1: "год", 2: "года", 3: "года", 4: "года"}.get(n % 10, "лет")


def format_student(rec: dict) -> str:
    """Красивый вывод: 'Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30'."""
    surname, *names = rec["fio"].split()
    initials = "".join(f"{n[0].upper()}." for n in names)
    age = student_age(rec)
    return (f"{surname} {initials}".strip()
            + f" ({rec['group']}), {age} {_years(age)}, GPA {rec['gpa']:.2f}")


def student_to_dict(rec: dict) -> dict:
    """Копия записи для сериализации: другой объект, ключи в порядке STUDENT_FIELDS.

    Перед копированием запись проверяется, чтобы битая не попала в файл.

    Raises:
        ValueError: если запись не проходит validate_student.
    """
    validate_student(rec)
    return {k: rec[k] for k in STUDENT_FIELDS}


def student_from_dict(d: dict) -> dict:
    """Десериализация: берёт ровно нужные ключи, приводит gpa к float, проверяет.

    Лишние ключи отбрасываются, пропущенные — ValueError. Нормализация та же,
    что у make_student, потому что запись собирается через него.

    Raises:
        ValueError: если d не словарь, нет какого-то поля или значение не подошло.
    """
    if not isinstance(d, dict):
        raise ValueError(f"запись должна быть объектом, получено {type(d).__name__}")
    missing = [k for k in STUDENT_FIELDS if k not in d]
    if missing:
        raise ValueError(f"нет полей: {missing}")
    return make_student(d["fio"], d["birthdate"], d["group"], d["gpa"])


def update_student(rec: dict, **fields) -> dict:
    """★ Новая запись с изменёнными полями; исходная не меняется.

    update_student(s1, gpa=4.8) -> новая запись, s1["gpa"] прежний.

    Raises:
        KeyError: если среди fields есть неизвестный ключ.
        ValueError: если новое значение не подошло.
    """
    unknown = sorted(set(fields) - set(STUDENT_FIELDS))
    if unknown:
        raise KeyError(f"неизвестные поля: {unknown}")
    # {**rec, **fields} — новый словарь, rec остаётся прежним
    return student_from_dict({**rec, **fields})
