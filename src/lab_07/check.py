import random
from src.lab_07.search import (
    linear_search,
    binary_search,
    two_sum_brute,
    two_sum_fast,)
from src.lab_07.sorting import (
    bubble_sort,
    insertion_sort,
    selection_sort,)

checks = 0
FIXED_LISTS = [
    [],
    [5],
    [2, 1],
    [1, 2],
    [2, 2, 2],
    [-3, 0, -3, 2],]

def random_list():
    """Создаёт случайный список длиной 0–50 со значениями -100–100."""
    n = random.randint(0, 50)
    return [random.randint(-100, 100) for _ in range(n)]

def check_sorting(fn, trials=100) -> None:
    """Сравнивает сортировку с sorted и проверяет неизменность входа."""
    global checks

    cases = [list(nums) for nums in FIXED_LISTS]
    cases += [random_list() for _ in range(trials)]

    for nums in cases:
        original = list(nums)
        result = fn(nums)

        message = (
            f"{fn.__name__}: "
            f"исходный={original}, результат={result}")

        assert result == sorted(original), message
        assert nums == original, f"Изменён исходный список: {message}"
        assert isinstance(result, list), f"Результат не список: {message}"
        assert result is not nums, f"Возвращён исходный список: {message}"

        checks += 1

def index_or_minus_one(nums, x):
    """Возвращает результат list.index или -1 при отсутствии x."""
    try:
        return nums.index(x)
    except ValueError:
        return -1

def check_search() -> None:
    """Проверяет оба поиска на случайных и граничных случаях."""
    global checks

    cases = [list(nums) for nums in FIXED_LISTS]
    cases += [random_list() for _ in range(100)]

    for nums in cases:
        ordered = sorted(nums)

        queries = [
            -101,
            101,
            random.randint(-100, 100),
            random.randint(-100, 100),]
        if ordered:
            queries += [ordered[0], ordered[-1]]
        else:
            queries += [0, 1]
        for x in queries:
            expected = index_or_minus_one(nums, x)
            actual = linear_search(nums, x)
            assert actual == expected, (
                f"linear_search: nums={nums}, x={x}, "
                f"ожидалось={expected}, получено={actual}")
            checks += 1

            expected = index_or_minus_one(ordered, x)
            actual = binary_search(ordered, x)

            if expected == -1:
                valid = actual == -1
            else:
                valid = (
                    0 <= actual < len(ordered)
                    and ordered[actual] == x)
            assert valid, (
                f"binary_search: nums={ordered}, x={x}, "
                f"получено={actual}, первое вхождение={expected}")
            checks += 1
def check_two_sum(trials=100) -> None:
    """Проверяет существование решения и корректность обеих пар."""
    global checks
    cases = [
        ([], 0),
        ([1], 2),
        ([3, 3], 6),
        ([1, 2], 10),
        ([-3, 1, 2, 5], 2),
        ([1, 2, 3, 4], 5),]

    for trial in range(trials):
        nums = random_list()
        target = random.randint(-200, 200)

        # В части случаев специально обеспечиваем существование пары.
        if trial % 2 == 0 and len(nums) >= 2:
            i, j = random.sample(range(len(nums)), 2)
            target = nums[i] + nums[j]

        cases.append((nums, target))
    for nums, target in cases:
        brute = two_sum_brute(nums, target)
        fast = two_sum_fast(nums, target)
        message = (
            f"nums={nums}, target={target}, "
            f"brute={brute}, fast={fast}")
        exists = any(
            nums[i] + nums[j] == target
            for i in range(len(nums))
            for j in range(i + 1, len(nums)))
        assert (brute is not None) == exists, message
        assert (fast is not None) == exists, message
        for pair in (brute, fast):
            if pair is not None:
                assert isinstance(pair, tuple) and len(pair) == 2, message
                i, j = pair
                assert 0 <= i < j < len(nums), message
                assert nums[i] + nums[j] == target, message
        checks += 1

def main():
    """Запускает все проверки и печатает их количество."""
    global checks
    checks = 0
    random.seed(42)
    for fn in (bubble_sort, insertion_sort, selection_sort):
        check_sorting(fn)
    check_search()
    check_two_sum()
    print(f"OK: {checks} проверок")
if __name__ == "__main__":
    main()