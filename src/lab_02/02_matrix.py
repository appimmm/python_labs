def transpose(mat: list[list[float | int]]) -> list[list]:
    """Поменять строки и столбцы местами. Пустая матрица [] -> [].
    Если матрица «рваная» (строки разной длины) — ValueError."""
    if not mat:
        return []
    
    cols = len(mat[0])
    for row in mat:
        if len(row) != cols:
            raise ValueError("рваная матрица")
            
    result = []
    for j in range(cols):
        new_row = []
        for i in range(len(mat)):
            new_row.append(mat[i][j])
        result.append(new_row)
    return result

def row_sums(mat: list[list[float | int]]) -> list[float]:   
    """Сумма по каждой строке. Требуется прямоугольность (см. выше)."""
    if not mat:
        return []
    
    cols = len(mat[0])
    sums = []
    
    for row in mat:
        if len(row) != cols:
            raise ValueError("рваная")
        current_sum = 0
        for num in row:
            current_sum += num
        sums.append(current_sum)
    return sums

def col_sums(mat: list[list[float | int]]) -> list[float]:
    """Сумма по каждому столбцу. Требуется прямоугольность."""
    if not mat:
        return []
    cols = len(mat[0])
    for row in mat:
        if len(row) != cols:
            raise ValueError("рваная")
            
    sums = [0] * cols
    for row in mat:
        for j in range(cols):
            sums[j] += row[j]
    return sums

print("transpose")
print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
try:
    print(transpose([[1, 2], [3]]))
except ValueError as e:
    print(f"ValueError: {e}")


print("\nrow_sums")
print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0, 0], [0, 0]]))
try:
    print(row_sums([[1, 2], [3]]))
except ValueError as e:
    print(f"ValueError: {e}")


print("\ncol_sums")
print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
try:
    print(col_sums([[1, 2], [3]]))
except ValueError as e:
    print(f"ValueError: {e}")