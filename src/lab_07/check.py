"""Запуск: python -m src.lab07.check (не использовать python -O)."""
import random
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

SORT_CASES = ([], [0], [2, 1], [1, 2], [2, 2], [-3, 0, -3, 2], [3, 2, 1])
SEARCH_CASES = ([], [5], [1, 2], [2, 1], [2, 2], [-3, 0, -3, 2])
PAIR_CASES = (([], 0), ([1], 2), ([3, 3], 6), ([1, 2], 10),
              ([-3, 1, 2, 5], 2), ([1, 2, 3, 4], 5))
_checks = 0
def record():
     """Увеличивает общий счётчик успешно пройденных проверок на единицу."""
    global _checks
    _checks += 1

def random_nums():
    """Возвращает случайный список длиной от 0 до 50 с числами от -100 до 100."""
    return [random.randint(-100, 100) for _ in range(random.randint(0, 50))]

def check_sorting(fn, trials=100) -> None:
    """Проверяет сортировку fn на случайных и фиксированных списках.

    Сравнивает результат с sorted, проверяет неизменность исходного
    списка и возврат нового списка. При ошибке вызывает AssertionError.
    trials задаёт количество случайных случаев.
    """
    for nums in [list(case) for case in SORT_CASES] + [random_nums() for _ in range(trials)]:
        original = list(nums)
        result = fn(nums)
        assert result == sorted(original), f'{fn.__name__}: nums={original}, result={result}'
        assert nums == original, f'{fn.__name__} изменила {original} на {nums}'
        assert isinstance(result, list) and result is not nums, f'{fn.__name__}: нужен новый список, nums={original}'
        record()

def index_or_minus_one(nums, x):
    """Возвращает индекс первого вхождения x через list.index или -1."""
    try:
        return nums.index(x)
    except ValueError:
        return -1

def check_search() -> None:
    """Проверяет линейный и бинарный поиск на случайных и граничных случаях.

    Использует list.index как эталон. Для бинарного поиска допускает
    любое вхождение искомого значения в отсортированном списке.
    При расхождении вызывает AssertionError с данными случая.
    """
    for nums in [list(case) for case in SEARCH_CASES] + [random_nums() for _ in range(100)]:
        ordered = sorted(nums)
        # Два случайных запроса, два гарантированных промаха, оба края.
        queries = [random.randint(-100, 100), random.randint(-100, 100), -101, 101]
        queries += [ordered[0], ordered[-1]] if ordered else [0, 1]
        for x in queries:
            expected = index_or_minus_one(nums, x)
            actual = linear_search(nums, x)
            assert actual == expected, f'linear: nums={nums}, x={x}, result={actual}, expected={expected}'
            record()
            expected = index_or_minus_one(ordered, x)
            actual = binary_search(ordered, x)
            valid = actual == -1 if expected == -1 else 0 <= actual < len(ordered) and ordered[actual] == x
            assert valid, f'binary: nums={ordered}, x={x}, result={actual}, first={expected}'
            record()

def check_two_sum(trials=100) -> None:
    """Проверяет оба решения Two Sum на случайных и фиксированных данных.

    Проверяет существование решения, корректность индексов и суммы.
    Допускает разные подходящие пары. При ошибке вызывает AssertionError.
    trials задаёт количество случайных случаев.
    """
    cases = list(PAIR_CASES)
    for k in range(trials):
        nums = random_nums()
        target = random.randint(-200, 200)
        if k % 2 == 0 and len(nums) >= 2:
            i, j = random.sample(range(len(nums)), 2)
            target = nums[i] + nums[j]
        cases.append((nums, target))
    for nums, target in cases:
        a, b = two_sum_brute(nums, target), two_sum_fast(nums, target)
        context = f'nums={nums}, target={target}, brute={a}, fast={b}'
        assert (a is None) == (b is None), context
        # Независимая проверка существования не пропустит общий ошибочный None.
        exists = any(nums[i] + nums[j] == target for i in range(len(nums)) for j in range(i + 1, len(nums)))
        assert (a is not None) == exists, context
        for pair in (a, b):
            if pair is not None:
                assert isinstance(pair, tuple) and len(pair) == 2, context
                i, j = pair
                assert 0 <= i < j < len(nums) and nums[i] + nums[j] == target, context
        record()

def main():
    """Сбрасывает счётчик, задаёт seed и запускает все проверки.

    При успешном завершении печатает OK и количество проверок.
    """
    global _checks
    _checks = 0
    random.seed(42)
    for fn in (bubble_sort, insertion_sort, selection_sort):
        check_sorting(fn)
    check_search()
    check_two_sum()
    print(f'OK: {_checks} проверок')
if __name__ == '__main__':
    main()
