import os
import sys
from pathlib import Path

# папка src — на уровень выше, чем папка этого файла
SRC_DIR = Path(__file__).resolve().parent.parent

# говорим Python искать модули ещё и там
sys.path.append(str(SRC_DIR))

from lib.text import normalize, tokenize, count_freq, top_n

def print_table(pairs: list[tuple[str, int]]) -> None:
    """Печатает пары «слово — частота» в виде выровненной таблицы.

    Ширина первого столбца подбирается по самому длинному слову,
    но не меньше ширины заголовка.

    Args:
        pairs: список пар (слово, частота).
    """
    if not pairs:
        return

    # не уже заголовка, иначе шапка разъедется
    width = max(len("слово"), max(len(word) for word, _ in pairs))
    header = f"{'слово':<{width}} | частота"

    print(header)
    # длина черты — по длине шапки, чтобы совпадала всегда
    print("-" * len(header))
    for word, count in pairs:
        print(f"{word:<{width}} | {count}")


def main(table_mode: bool = False) -> None:
    """Считывает текст из стандартного ввода, нормализует его, разбивает на токены,
    считает частоту встречаемости токенов и выводит n наиболее часто встречающихся токенов.

    Args:
        table_mode: если True, выводит результат в виде таблицы.
    """
    text = sys.stdin.read()
    normalized_text = normalize(text)
    tokenize_text = tokenize(normalized_text)
    freq = count_freq(tokenize_text)
    top_tokens = top_n(freq, n=5)

    print("Всего слов:", len(tokenize_text))
    print("Уникальных слов:", len(freq))
    print("Топ-5:")

    if table_mode:
        print_table(top_tokens)
    else:
        for word, count in top_tokens:
            print(f"{word}:{count}")


if __name__ == "__main__":
    # TABLE_MODE=1 включает таблицу, без неё — обычный вывод
    main(table_mode=os.environ.get("TABLE_MODE") == "1")