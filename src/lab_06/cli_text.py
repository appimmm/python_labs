import argparse
from pathlib import Path

from src.lib.text import normalize, tokenize, count_freq, top_n
def main():
    """
    Обрабатывает аргументы командной строки.

    cat --input <path> [-n] — выводит содержимое файла.
    stats --input <txt> [--top 5] — выводит частоты слов.
    """
    parser = argparse.ArgumentParser(
        description="Вывод файлов и анализ частот слов")
    subparsers = parser.add_subparsers(
        dest="command",
        required=True)

    cat_parser = subparsers.add_parser(
        "cat",
        help="Вывести содержимое файла",
        description="Выводит файл построчно.")
    cat_parser.add_argument(
        "--input",
        required=True,
        help="Путь к входному файлу")
    cat_parser.add_argument(
        "-n",
        action="store_true",
        help="Нумеровать строки")

    stats_parser = subparsers.add_parser(
        "stats",
        help="Показать частоты слов",
        description="Выводит количество слов и наиболее частые слова.")
    stats_parser.add_argument(
        "--input",
        required=True,
        help="Путь к текстовому файлу")
    stats_parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Количество слов в топе (по умолчанию 5)")

    args = parser.parse_args()

    if args.command == "stats" and args.top <= 0:
        parser.error("--top должен быть положительным числом")

    path = Path(args.input)

    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {path}")

    if args.command == "cat":
        with path.open(encoding="utf-8") as file:
            for number, line in enumerate(file, start=1):
                if args.n:
                    print(f"{number}: ", end="")

                print(line, end="")

    elif args.command == "stats":
        with path.open(encoding="utf-8") as file:
            text = file.read()

        tokens = tokenize(normalize(text))
        freq = count_freq(tokens)
        top_words = top_n(freq, n=args.top)

        print(f"Всего слов: {len(tokens)}")
        print(f"Уникальных слов: {len(freq)}")
        print(f"Топ-{args.top}:")

        for word, count in top_words:
            print(f"{word}: {count}")
if __name__ == "__main__":
    main()