import csv
from pathlib import Path
def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Читает текстовый файл в указанной кодировке."""
    p = Path(path)
    return p.read_text(encoding=encoding)

def ensure_parent_dir(path: str | Path) -> None:
    """Создаёт родительские папки, если они отсутствуют."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

def write_csv(rows: list[tuple | list], path: str | Path, header: tuple[str, ...] | None = None) -> None:
    """Записывает строки в CSV и проверяет их длину."""
    if rows:
        expected_length = len(rows[0])

        for row in rows:
            if len(row) != expected_length:
                raise ValueError("Строки имеют разную длину")

        if header is not None and len(header) != expected_length:
            raise ValueError("Длина заголовка не совпадает с длиной строк")

    ensure_parent_dir(path)

    with Path(path).open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")

        if header is not None:
            writer.writerow(header)

        writer.writerows(rows)


if __name__ == "__main__":
    text = read_text("data/lab_04/input.txt")
    print("Прочитанный текст:")
    print(text)

    write_csv([("привет", 2), ("мир", 1)],
            "data/lab04/check.csv",
            header=("word", "count"))

    print("CSV-файл успешно создан!")