import argparse
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(SRC_DIR))

from lib.text import normalize, tokenize, count_freq, top_n
from io_txt_csv import read_text, write_csv, ensure_parent_dir


def main() -> None:
    """Считает частоты слов во входных файлах и сохраняет отчёты в CSV.

    Без аргументов читает data/Lab04/input.txt и пишет data/Lab04/report.csv.
    Если передано несколько путей в --in, частоты суммируются по всем файлам,
    а с флагом --per-file дополнительно сохраняется разбивка по файлам.

    Пустой входной файл не считается ошибкой: отчёт создаётся и содержит
    только строку заголовка.

    Returns:
        None. Результат — файлы на диске и резюме в консоли.

    Raises:
        FileNotFoundError: если входного файла нет.
        UnicodeDecodeError: если файл не читается в указанной кодировке.
    """
    parser = argparse.ArgumentParser(description="Отчёт по частотам слов")
    parser.add_argument("--in", dest="inp", nargs="+",
                        default=["data/Lab04/input.txt"],
                        help="пути к входным файлам (один или больше)")
    parser.add_argument("--out", dest="out", default="data/Lab04/report.csv",
                        help="куда сохранить отчёт word,count")
    parser.add_argument("--per-file", dest="per_file", default=None,
                        help="куда сохранить разбивку file,word,count")
    parser.add_argument("--total", dest="total", default=None,
                        help="куда сохранить сводный отчёт (иначе --out)")
    parser.add_argument("--encoding", default="utf-8",
                        help="кодировка входных файлов, например cp1251")
    args = parser.parse_args()

    all_tokens = []
    per_file_rows = []

    for p in args.inp:
        text = read_text(p, encoding=args.encoding)
        tokens = tokenize(normalize(text))
        all_tokens.extend(tokens)

        name = Path(p).name
        for word, count in count_freq(tokens).items():
            per_file_rows.append((name, word, count))

    freq = count_freq(all_tokens)
    rows = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

    total_path = args.total or args.out
    ensure_parent_dir(total_path)
    write_csv(rows, total_path, header=("word", "count"))

    if args.per_file:
        per_file_rows.sort(key=lambda r: (r[0], -r[2], r[1]))
        ensure_parent_dir(args.per_file)
        write_csv(per_file_rows, args.per_file,
                  header=("file", "word", "count"))

    print("Всего слов:", len(all_tokens))
    print("Уникальных слов:", len(freq))
    print("Топ-5:")
    for word, count in top_n(freq, 5):
        print(f"{word}:{count}")


if __name__ == "__main__":
    main()
