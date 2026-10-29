import argparse

from src.Lab04.io_txt_csv import ensure_parent_dir
from src.Lab05.csv_xlsx import csv_to_xlsx
from src.Lab05.json_csv import csv_to_json, json_to_csv



def main() -> None:
    """Запускает CLI-конвертеры из ЛР5 с подкомандами json2csv, csv2json, csv2xlsx.

    У каждой подкоманды два обязательных флага: --in (входной файл) и
    --out (выходной). Папка под выходной файл создаётся, если её нет.

    Запускать из корня проекта: python -m src.Lab06.cli_convert <подкоманда>.
    Для csv2xlsx нужен openpyxl, то есть запуск из виртуального окружения.

    Returns:
        None.

    Raises:
        FileNotFoundError: если входного файла нет.
        ValueError: если входные данные пусты или неподходящей структуры
            (бросают функции из ЛР5).
    """
    parser = argparse.ArgumentParser(description="Конвертеры данных")
    sub = parser.add_subparsers(dest="cmd", required=True)

    for name, help_text in [("json2csv", "JSON в CSV"),
                            ("csv2json", "CSV в JSON"),
                            ("csv2xlsx", "CSV в XLSX")]:
        p = sub.add_parser(name, help=help_text)
        # in — ключевое слово Python, args.in написать нельзя, поэтому dest
        p.add_argument("--in", dest="input", required=True, help="входной файл")
        p.add_argument("--out", dest="output", required=True, help="выходной файл")

    args = parser.parse_args()
    # без этого запись в data/out/... упадёт, если папки ещё нет
    ensure_parent_dir(args.output)
    if args.cmd == "json2csv":
        json_to_csv(args.input, args.output)
    elif args.cmd == "csv2json":
        csv_to_json(args.input, args.output)
    elif args.cmd == "csv2xlsx":
        csv_to_xlsx(args.input, args.output)


if __name__ == "__main__":
    main()

