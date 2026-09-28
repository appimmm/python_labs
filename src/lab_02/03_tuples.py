def format_record(rec: tuple[str, str, float | int]) -> str:
    """
    Форматирует кортеж студента в строку вида "Фамилия И.О., гр. ГРУППА, GPA X.XX".
    Ожидает кортеж (ФИО, группа, GPA).
    
    Ошибки:
    - TypeError: если GPA не число.
    - ValueError: если ФИО или группа пустые, ФИО содержит менее двух слов, 
                  или GPA выходит за пределы [0.0, 5.0].
    """
    if len(rec) != 3:
        raise ValueError("Запись должна содержать ровно 3 элемента")
        
    fio_raw, group_raw, gpa = rec
    
    if not isinstance(gpa, (float, int)):
        raise TypeError("GPA должен быть числом")
        
    if not (0.0 <= gpa <= 5.0):
        raise ValueError("GPA должен быть в диапазоне от 0.0 до 5.0")
        
    fio_parts = str(fio_raw).split()
    if len(fio_parts) < 2:
        raise ValueError("ФИО должно содержать хотя бы фамилию и имя")
        
    group = str(group_raw).strip()
    if not group:
        raise ValueError("Группа не может быть пустой")
        
    last_name = fio_parts[0].capitalize()
    
    initials = ""
    for part in fio_parts[1:3]:
        initials += part[0].upper() + "."
    return f"{last_name} {initials}, гр. {group}, GPA {gpa:.2f}"


print(format_record(("Иванов Иван Иванович", "BIVT-25", 4.6)))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))


try:
    print(format_record((" ", "BIVT-25", 4.0)))
except ValueError as e:
    print(f"ValueError: {e}")

try:
    print(format_record(("Иванов Иван", "   ", 4.0)))
except ValueError as e:
    print(f"ValueError: {e}")

try:
    print(format_record(("Иванов Иван", "BIVT-25", "пять")))
except TypeError as e:
    print(f"TypeError: {e}")