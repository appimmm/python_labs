import multiprocessing as mp
from pathlib import Path
import random
import timeit
from src.lab_04.io_txt_csv import write_csv
from src.lab_07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab_07.sorting import bubble_sort, insertion_sort, selection_sort

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "data" / "lab07" / "bench.csv"
TIME_LIMIT = 60

def sort_worker(fn, data, connection):
    """Измеряет сортировку в отдельном процессе."""
    try:
        connection.send(("ready", None))
        seconds = timeit.timeit(lambda: fn(data), number=1)
        connection.send(("ok", seconds))
    except Exception as error:
        connection.send(("error", repr(error)))
    finally:
        connection.close()

def timed_sort(fn, data):
    """Возвращает время сортировки или отметку о превышении лимита."""
    context = mp.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    process = context.Process(target=sort_worker, args=(fn, data, sender))
    process.start()
    sender.close()
    try:
        if not receiver.poll(30):
            raise RuntimeError("Не удалось запустить процесс сортировки")
        status, value = receiver.recv()
        if status != "ready":
            raise RuntimeError(value)
        if receiver.poll(TIME_LIMIT):
            status, value = receiver.recv()
            if status == "ok":
                return value
            raise RuntimeError(value)
        return f"> {TIME_LIMIT} с"
    finally:
        if process.is_alive():
            process.terminate()
        process.join()
        receiver.close()

def save_result(rows, task, n, impl, seconds):
    """Выводит результат и сохраняет CSV."""
    value = f"{seconds:.9f}" if isinstance(seconds, float) else seconds
    rows.append((task, n, impl, value))
    print(f"{task:<18}  {n:>8}  {impl:<20}  {value:>16}", flush=True)
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_csv(rows, CSV_PATH, header=("task", "n", "impl", "seconds"))

def bench_sorts(rows):
    """Сравнивает сортировки на одинаковых случайных данных."""
    for n in (1_000, 10_000, 100_000):
        data = [random.randint(-100_000, 100_000) for _ in range(n)]
        for fn in (bubble_sort, insertion_sort, selection_sort, sorted):
            if n == 100_000 and fn in (bubble_sort, insertion_sort, selection_sort):
                seconds = timed_sort(fn, data)
            else:
                seconds = timeit.timeit(lambda: fn(data), number=1)
            save_result(rows, "sort", n, fn.__name__, seconds)

def run_queries(fn, nums, queries):
    """Выполняет все поисковые запросы."""
    for x in queries:
        fn(nums, x)

def bench_search(rows):
    """Сравнивает 10 000 запросов и отдельно измеряет сортировку."""
    n = 100_000
    data = [random.randint(-100_000, 100_000) for _ in range(n)]
    queries = [random.randint(-100_000, 100_000) for _ in range(10_000)]
    seconds = timeit.timeit(lambda: sorted(data), number=1)
    save_result(rows, "search_prepare", n, "sorted", seconds)
    ordered = sorted(data)
    for fn, nums in ((linear_search, data), (binary_search, ordered)):
        seconds = timeit.timeit(lambda: run_queries(fn, nums, queries), number=1)
        save_result(rows, "search", n, fn.__name__, seconds)

def bench_two_sum(rows):
    """Сравнивает Two Sum на данных с единственной парой в конце."""
    for n in (1_000, 10_000):
        data = [random.randint(1, 100_000) for _ in range(n - 2)]
        data += [-1, -2]
        target = -3
        for fn in (two_sum_brute, two_sum_fast):
            seconds = timeit.timeit(lambda: fn(data, target), number=1)
            save_result(rows, "two_sum", n, fn.__name__, seconds)

def main():
    """Запускает обязательные замеры."""
    random.seed(42)
    rows = []
    print(f"{'Задача':<18}  {'Размер':>8}  {'Алгоритм':<20}  {'Время(с)':>16}", flush=True)
    bench_sorts(rows)
    bench_search(rows)
    bench_two_sum(rows)
    print(f"\nРезультаты сохранены: {CSV_PATH}")

if __name__ == "__main__":
    main()