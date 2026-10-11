import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.text import normalize, tokenize, count_freq, top_n
from lab_04.io_txt_csv import read_text, write_csv

def frequencies_from_text(text: str) -> dict[str, int]:
    """Считает частоту каждого слова в тексте."""
    tokens = tokenize(normalize(text))
    return count_freq(tokens)
def sorted_word_counts(freq: dict[str, int]) -> list[tuple[str, int]]:
    """Сортирует слова по частоте и алфавиту."""
    return sorted(freq.items(), key=lambda item: (-item[1], item[0]))
def main() -> None:
    """Создаёт CSV-отчёт по входному текстовому файлу."""
    parser = argparse.ArgumentParser(description="Отчёт по частотам слов")

    parser.add_argument("--in", dest="input_path", default="data/lab_04/input.txt")
    parser.add_argument("--out", default="data/lab_04/report.csv")
    parser.add_argument("--encoding", default="utf-8")

    args = parser.parse_args()

    try:
        text = read_text(args.input_path, encoding=args.encoding)
    except (FileNotFoundError, UnicodeDecodeError) as error:
        print(f"Ошибка чтения файла: {error}", file=sys.stderr)
        sys.exit(1)

    freq = frequencies_from_text(text)
    rows = sorted_word_counts(freq)

    write_csv(rows, args.out, header=("word", "count"))

    print(f"Всего слов: {sum(freq.values())}")
    print(f"Уникальных слов: {len(freq)}")
    print("Топ-5:")

    for word, count in top_n(freq, n=5):
        print(f"{word}:{count}")
if __name__ == "__main__":
    main()