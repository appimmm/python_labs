# Лабораторная работа 1

# Задание 1
```python
import re

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    """
    Очищает текст: приводит к нужному регистру, заменяет 'ё' на 'е' (по умолчанию),
    схлопывает любые переносы строк и пробелы в один пробел, обрезает края.
    """
    if casefold:
        text = text.casefold()
    else:
        text = text.lower()
        
    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')
        
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def tokenize(text: str) -> list[str]:
    """
    Разбивает текст на слова (токены) по шаблону.
    Сохраняет буквы, цифры и дефисы внутри слов, отбрасывая знаки препинания.
    """
    return re.findall(r'\w+(?:-\w+)*', text)


def count_freq(tokens: list[str]) -> dict[str, int]:
    """
    Принимает список слов и считает, сколько раз каждое из них встречается.
    Возвращает словарь формата {'слово': количество}.
    """
    freq = {}
    for word in tokens:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """
    Возвращает топ-N самых частых слов. 
    Сортирует по убыванию частоты, а при одинаковой частоте — по алфавиту.
    """
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:n]
if __name__ == '__main__':

    assert normalize("ПрИвЕт\nМИр\t") == "привет мир"
    assert normalize("ёжик, Ёлка", yo2e=True) == "ежик, елка"
    assert normalize("Hello\r\nWorld") == "hello world"
    assert normalize("  двойные  пробелы  ") == "двойные пробелы"

    assert tokenize("привет мир") == ["привет", "мир"]
    assert tokenize("hello,world!!!") == ["hello", "world"]
    assert tokenize("по-настоящему круто") == ["по-настоящему", "круто"]
    assert tokenize("2025 год") == ["2025", "год"]
    assert tokenize("emoji 😜 не слово") == ["emoji", "не", "слово"]

    assert count_freq(["a", "b", "a", "c", "b", "a"]) == {"a": 3, "b": 2, "c": 1}
    assert top_n(count_freq(["a", "b", "a", "c", "b", "a"]), n=2) == [("a", 3), ("b", 2)]

    assert count_freq(["bb", "aa", "bb", "aa", "cc"]) == {"aa": 2, "bb": 2, "cc": 1}
    assert top_n(count_freq(["bb", "aa", "bb", "aa", "cc"]), n=2) == [("aa", 2), ("bb", 2)]



    print("normalize")
    print(normalize("ПрИвЕт\nМИр\t"))
    print(normalize("ёжик, Ёлка", yo2e=True))
    print(normalize("Hello\r\nWorld"))
    print(normalize("  двойные  пробелы  "))

    print("\ntokenize")
    print(tokenize("привет мир"))
    print(tokenize("hello,world!!!"))
    print(tokenize("по-настоящему круто"))
    print(tokenize("2025 год"))
    print(tokenize("emoji 😜 не слово"))

    print("\ncount_freq+top_n")
    print("Словарь 1:", count_freq(["a", "b", "a", "c", "b", "a"]))
    print("Топ-2:", top_n(count_freq(["a", "b", "a", "c", "b", "a"]), n=2))

    print("Словарь 2:", count_freq(["bb", "aa", "bb", "aa", "cc"]))
    print("Топ-2 (проверка алфавита):", top_n(count_freq(["bb", "aa", "bb", "aa", "cc"]), n=2))
```
![Задание 1](images/lab_03/01_A.png)
# Задание 2
```python
import sys
from lib.text import normalize, tokenize, count_freq, top_n
deff_kr = True
if __name__ == '__main__':
    text = sys.stdin.read()
    
    if not text.strip():
        sys.exit(0)

    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    top_words = top_n(freq, n=5)

    if not deff_kr:
        print(f"Всего слов: {len(tokens)}")
        print(f"Уникальных слов: {len(freq)}")
        print("Топ-5:")
        for word, count in top_words:
            print(f"{word}:{count}")
    else:
        if top_words:
            max_len = max(len(w) for w, _ in top_words)
            max_len = max(max_len, 5) 
            print(f"{'слово':<{max_len}} | частота")
            print("-" * (max_len + 10))
            for word, count in top_words:
                print(f"{word:<{max_len}} | {count}")
```
![Задание 2](images/lab_03/02_B.png)
![Задание 2](images/lab_03/03_BB.png)