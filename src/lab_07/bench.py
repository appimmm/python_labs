import multiprocessing as mp
from pathlib import Path
import random
import timeit
from src.lab04.io_txt_csv import write_csv
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

ROOT = Path(__file__).resolve().parents[2]
LIMIT = 60

def _worker(fn, data, connection):
    """Измеряет время одного вызова fn(data) в отдельном процессе.

    Передаёт время или сообщение об ошибке через канал связи,
    затем закрывает свой конец канала.
    """
    try:
        # Генерация, запуск процесса и передача данных не входят в timeit.
        connection.send(('ok', timeit.timeit(lambda: fn(data), number=1)))
    except Exception as error:
        connection.send(('error', repr(error)))
    finally:
        connection.close()

def limited_sort(fn, data):
    """Запускает сортировку в отдельном процессе с ограничением времени.

    Возвращает время сортировки в секундах или строку о превышении лимита.
    При ошибке в рабочем процессе вызывает RuntimeError.
    Перед выходом завершает процесс и закрывает принимающий конец канала.
    """
    context = mp.get_context('spawn')
    receiver, sender = context.Pipe(duplex=False)
    process = context.Process(target=_worker, args=(fn, data, sender))
    process.start()
    sender.close()
    try:
        if receiver.poll(LIMIT):
            status, value = receiver.recv()
            if status != 'ok':
                raise RuntimeError(value)
            return value
        return f'> {LIMIT} с'
    finally:
        if process.is_alive():
            process.terminate()
        process.join()
        receiver.close()

def bench_sorts(n):
     """Измеряет три ручные сортировки и sorted на одном списке длины n.

    Для ручных сортировок при n = 100 000 применяет ограничение времени.
    Возвращает строки результатов: задача, размер, алгоритм, секунды.
    """
    data = [random.randint(-100_000, 100_000) for _ in range(n)]
    rows = []
    for fn in (bubble_sort, insertion_sort, selection_sort, sorted):
        seconds = limited_sort(fn, data) if n == 100_000 and fn is not sorted else timeit.timeit(lambda: fn(data), number=1)
        rows.append(('sort', n, fn.__name__, seconds))
    return rows

def run_queries(fn, nums, queries):
    """Выполняет поиск функцией fn в списке nums для каждого запроса."""
    for x in queries:
        fn(nums, x)

def main():
    random.seed(42)
    rows = []
    def save(new_rows):
        for task, n, impl, seconds in new_rows:
            value = f'{seconds:.9f}' if isinstance(seconds, float) else seconds
            rows.append((task, n, impl, value))
            print(f'{task:<14} {n:>8} {impl:<20} {value:>16}', flush=True)
        write_csv(rows, ROOT / 'data/lab07/bench.csv', header=('task', 'n', 'impl', 'seconds'))
    print(f'{"task":<14} {"n":>8} {"impl":<20} {"seconds":>16}', flush=True)
    for n in (1_000, 10_000, 100_000):
        save(bench_sorts(n))
    n = 100_000
    data = [random.randint(-100_000, 100_000) for _ in range(n)]
    queries = [random.randint(-100_000, 100_000) for _ in range(10_000)]
    save([('search_prepare', n, 'sorted', timeit.timeit(lambda: sorted(data), number=1))])
    ordered = sorted(data)
    for fn, nums in ((linear_search, data), (binary_search, ordered)):
        seconds = timeit.timeit(lambda: run_queries(fn, nums, queries), number=1)
        save([('search', n, fn.__name__, seconds)])
    for n in (1_000, 10_000):
        # Только последняя пара даёт -3: исключаем случайный ранний ответ.
        data = [random.randint(1, 100_000) for _ in range(n - 2)] + [-1, -2]
        for fn in (two_sum_brute, two_sum_fast):
            save([('two_sum', n, fn.__name__, timeit.timeit(lambda: fn(data, -3), number=1))])
if __name__ == '__main__':
    main()
