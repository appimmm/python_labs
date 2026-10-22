import argparse
from src.lab_05.json_csv import json_to_csv, csv_to_json

def main():
    """
    Обрабатывает аргументы и вызывает функции конвертации из ЛР5.

    json2csv --in <json> --out <csv> — преобразует JSON в CSV.
    csv2json --in <csv> --out <json> — преобразует CSV в JSON.
    csv2xlsx --in <csv> --out <xlsx> — преобразует CSV в XLSX.
    """
    parser = argparse.ArgumentParser(
        description="Конвертация JSON, CSV и XLSX"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True)

    json_parser = subparsers.add_parser(
        "json2csv",
        help="Преобразовать JSON в CSV",
        description="Преобразует список словарей JSON в CSV.")
    json_parser.add_argument(
        "--in",
        dest="input",
        required=True,
        help="Путь к входному JSON-файлу")
    json_parser.add_argument(
        "--out",
        dest="output",
        required=True,
        help="Путь к выходному CSV-файлу")

    csv_parser = subparsers.add_parser(
        "csv2json",
        help="Преобразовать CSV в JSON",
        description="Преобразует CSV с заголовком в JSON.")
    csv_parser.add_argument(
        "--in",
        dest="input",
        required=True,
        help="Путь к входному CSV-файлу")
    csv_parser.add_argument(
        "--out",
        dest="output",
        required=True,
        help="Путь к выходному JSON-файлу")

    xlsx_parser = subparsers.add_parser(
        "csv2xlsx",
        help="Преобразовать CSV в XLSX",
        description="Преобразует CSV в Excel-файл.")
    xlsx_parser.add_argument(
        "--in",
        dest="input",
        required=True,
        help="Путь к входному CSV-файлу")
    xlsx_parser.add_argument(
        "--out",
        dest="output",
        required=True,
        help="Путь к выходному XLSX-файлу")

    args = parser.parse_args()

    try:
        if args.command == "json2csv":
            json_to_csv(args.input, args.output)

        elif args.command == "csv2json":
            csv_to_json(args.input, args.output)

        elif args.command == "csv2xlsx":
            from src.lab_05.csv_xlsx import csv_to_xlsx

            csv_to_xlsx(args.input, args.output)

    except ValueError as error:
        parser.error(str(error))

    print(f"Файл создан: {args.output}")
if __name__ == "__main__":
    main()