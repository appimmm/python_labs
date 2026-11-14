def linear_search(nums, x) -> int:
    """Возвращает индекс первого вхождения x или -1."""
    for i, value in enumerate(nums):
        if value == x:
            return i
    return -1

def binary_search(sorted_nums, x) -> int:
    """Возвращает индекс любого вхождения x или -1.
    Список должен быть отсортирован по возрастанию.
    На неотсортированном списке результат не определён.
    """
    lo = 0
    hi = len(sorted_nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_nums[mid] == x:
            return mid
        if sorted_nums[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def two_sum_brute(nums, target) -> tuple[int, int] | None:
    """Перебирает пары и возвращает индексы i < j с суммой target.
    Если подходящей пары нет, возвращает None.
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return i, j
    return None

def two_sum_fast(nums, target) -> tuple[int, int] | None:
    """Находит пару с суммой target за один проход со словарём.

    Возвращает индексы i < j или None, если решения нет.
    """
    seen = {}
    for j, value in enumerate(nums):
        needed = target - value
        if needed in seen:
            return seen[needed], j
        seen[value] = j
    return None