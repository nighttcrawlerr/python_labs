def format_record(rec: tuple[str, str, float]) -> str:
    """Форматирует запись студента в строку для печати.

    Запись — кортеж (ФИО, группа, GPA). ФИО может быть в виде
    «Фамилия Имя Отчество» или «Фамилия Имя»; лишние пробелы убираются,
    инициалы формируются из имён в верхнем регистре, GPA печатается
    с двумя знаками после запятой.

    Args:
        rec: кортеж из трёх элементов — ФИО (str), группа (str), GPA (float).

    Returns:
        Строка вида "Иванов И.И., гр. BIVT-25, GPA 4.60".

    Raises:
        TypeError: если GPA не число либо ФИО или группа не строки или если rec не кортеж.
        ValueError: если ФИО содержит меньше двух частей (нет имени),
            группа пустая, либо gpa не в диапазоне 0.0 <= GPA <= 5.0, либо rec не кортеж из 3-х элементов.
    """
    if not isinstance(rec, tuple):
        raise TypeError("rec должен быть кортежем")
    if len(rec) != 3:
        raise ValueError("rec должен содержать ровно три элемента")
    fio, group, gpa = rec
    if not isinstance(gpa, (int, float)):
        raise TypeError("gpa должен быть числом")
    if not isinstance(fio, str) or not isinstance(group, str):
        raise TypeError("ФИО и группа должны быть строками")

    part = fio.split()
    if len(part) <= 1:
        raise ValueError("ФИО должно содержать фамилию и имя")

    if not (0.0 <= gpa <= 5.0):
        raise ValueError("Оценка может быть только от 0 до 5")

    group = group.strip()
    if not group:
        raise ValueError("Группа должна быть указана")

    surname = part[0].capitalize()
    first_let = (p[0].upper() + '.' for p in part[1:])
    initials = ''.join(first_let)
    return f"{surname} {initials}, гр. {group}, GPA {gpa:.2f}"


if __name__ == "__main__":
    fio = input("Введите ФИО: ")
    group = input("Введите группу: ")
    gpa = float(input("Введите GPA: "))

    rec = (fio, group, gpa)
    print(format_record(rec))
