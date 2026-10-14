import re

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    """Нормализует текст.

    Нормализация включает в себя:
    - удаление лишних пробелов (в начале, в конце, между словами);
    - приведение к нижнему регистру (если casefold=True);
    - замену буквы "ё" на "е" (если yo2e=True).

    Args:
        text: исходный текст.
        casefold: если True, приводит текст к нижнему регистру.
        yo2e: если True, заменяет букву "ё" на "е".

    Returns:
        Нормализованный текст.
    """
    # split() без аргументов сам режет по \t \r \n и схлопывает пробелы
    text = ' '.join(text.split())
    if casefold:
        text = text.casefold()
    else:
        text = text.lower()
    if yo2e:
        text = text.replace('ё', 'е')
    return text


def tokenize(text: str) -> list[str]:
    """Разбивает текст на токены.

    Токен — это последовательность букв и цифр, подчеркивания и дефисы внутри слова, разделённая пробелами
    или знаками препинания. Знаки препинания не включаются в токены.

    Args:
        text: исходный текст.

    Returns:
        Список токенов.
    """
    # дефис только внутри слова: "по-настоящему" целиком, "-слово" без дефиса
    return re.findall(r'\w+(?:-\w+)*', text)


def count_freq(tokens: list[str]) -> dict[str, int]:
    """Считает частоту встречаемости токенов.

    Args:
        tokens: список токенов.

    Returns:
        Словарь, где ключ — токен, а значение — количество его вхождений в список.
    """
    freq = {}
    for token in tokens:
        # get вернёт 0, если слово встретилось впервые
        freq[token] = freq.get(token, 0) + 1
    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Возвращает n наиболее часто встречающихся токенов.

    Args:
        freq: словарь частот токенов.
        n: сколько токенов вернуть; если n больше размера словаря,
            вернутся все.

    Returns:
        Список кортежей (токен, частота): по убыванию частоты, а при
        равной частоте — по алфавиту слова.

    Raises:
        ValueError: если n отрицательное.
    """
    if n < 0:
        raise ValueError("n не может быть отрицательным")
    # минус у частоты — чтобы шло по убыванию, слово — по алфавиту
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:n]


if __name__ == "__main__":
    print("--- normalize ---")
    print(normalize("ПрИвЕт\nМИр\t"))
    print(normalize("ёжик, Ёлка"))
    print(normalize("Hello\r\nWorld"))
    print(normalize("  двойные   пробелы  "))

    print("--- tokenize ---")
    print(tokenize("привет мир"))
    print(tokenize("привет, мир!"))
    print(tokenize("hello,world!!!"))
    print(tokenize("по-настоящему круто"))
    print(tokenize("2025 год"))
    print(tokenize("emoji 😀 не слово"))

    print("--- count_freq ---")
    freq = count_freq(["a", "b", "a", "c", "b", "a"])
    print(freq)
    freq2 = count_freq(["bb", "aa", "bb", "aa", "cc"])
    print(freq2)

    print("--- top_n ---")
    print(top_n(freq, 2))
    # при равной частоте — по алфавиту: aa раньше bb
    print(top_n(freq2, 2))