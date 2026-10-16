import csv
import json
from pathlib import Path

def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Преобразует JSON-файл в CSV.
    Поддерживает список словарей [{...}, {...}], заполняет отсутствующие поля пустыми строками.
    Кодировка UTF-8. Порядок колонок — как в первом объекте или алфавитный (указать в README).
    """
    json_path = Path(json_path)
    csv_path = Path(csv_path)

    if not json_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {json_path}")

    if json_path.suffix.lower() != ".json":
        raise ValueError("Входной файл должен иметь расширение .json")

    if csv_path.suffix.lower() != ".csv":
        raise ValueError("Выходной файл должен иметь расширение .csv")

    with json_path.open(encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                "Пустой JSON или неподдерживаемая структура"
            ) from error

    if not isinstance(data, list) or not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    if any(not isinstance(row, dict) for row in data):
        raise ValueError("JSON должен содержать список словарей")

    columns = []

    for row in data:
        for key in row:
            if key not in columns:
                columns.append(key)

    if not columns:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    if any(not key.strip() for key in columns):
        raise ValueError("Названия столбцов не должны быть пустыми")

    with csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=columns,
            restval=""
        )
        writer.writeheader()
        writer.writerows(data)
def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Преобразует CSV в JSON (список словарей).
    Заголовок обязателен, значения сохраняются как строки.
    json.dump(..., ensure_ascii=False, indent=2)
    """
    csv_path = Path(csv_path)
    json_path = Path(json_path)

    if not csv_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {csv_path}")

    if csv_path.suffix.lower() != ".csv":
        raise ValueError("Входной файл должен иметь расширение .csv")

    if json_path.suffix.lower() != ".json":
        raise ValueError("Выходной файл должен иметь расширение .json")

    with csv_path.open(encoding="utf-8", newline="") as file:
        try:
            reader = csv.DictReader(file, strict=True)
            columns = reader.fieldnames

            if not columns:
                raise ValueError("Пустой CSV или отсутствует заголовок")

            if any(not name.strip() for name in columns):
                raise ValueError("Названия столбцов не должны быть пустыми")

            if len(columns) != len(set(columns)):
                raise ValueError("Названия столбцов не должны повторяться")

            data = []

            for row in reader:
                if None in row or None in row.values():
                    raise ValueError(
                        "Количество полей не совпадает с заголовком"
                    )

                data.append(row)

        except csv.Error as error:
            raise ValueError("Некорректный формат CSV") from error

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)