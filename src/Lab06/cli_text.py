import argparse

from src.Lab04.io_txt_csv import read_text
from src.lib.text import normalize, tokenize, count_freq, top_n


def main() -> None:
    """Запускает CLI с подкомандами cat и stats.

    cat --input FILE [-n]: печатает файл построчно, с флагом -n — с номерами.
    stats --input FILE [--top N]: считает слова функциями из lib/text.py,
    печатает всего слов, уникальных слов и топ-N (по умолчанию 5).

    Запускать из корня проекта: python -m src.Lab06.cli_text <подкоманда>.

    Returns:
        None.

    Raises:
        FileNotFoundError: если входного файла нет.
        UnicodeDecodeError: если файл не в UTF-8.
    """
    parser = argparse.ArgumentParser(description="CLI-утилиты для текста")
    sub = parser.add_subparsers(dest="command", required=True)

    cat_p = sub.add_parser("cat", help="вывести файл построчно")
    cat_p.add_argument("--input", required=True, help="путь к файлу")
    cat_p.add_argument("-n", action="store_true", help="нумеровать строки")

    stats_p = sub.add_parser("stats", help="частоты слов")
    stats_p.add_argument("--input", required=True, help="путь к текстовому файлу")
    stats_p.add_argument("--top", type=int, default=5, help="сколько слов в топе")

    args = parser.parse_args()

    if args.command == "cat":
        text = read_text(args.input)
        # enumerate(..., 1) — нумерация с единицы, а не с нуля
        for i, line in enumerate(text.splitlines(), 1):
            print(f"{i}: {line}" if args.n else line)
    elif args.command == "stats":
        # цепочка из ЛР3: нормализовать -> разбить на слова -> посчитать
        tokens = tokenize(normalize(read_text(args.input)))
        freq = count_freq(tokens)
        print("Всего слов:", len(tokens))
        print("Уникальных слов:", len(freq))
        print(f"Топ-{args.top}:")
        for word, count in top_n(freq, args.top):
            print(f"{word}:{count}")



if __name__ == "__main__":
    main()
