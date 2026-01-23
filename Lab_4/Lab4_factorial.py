import timeit
import matplotlib.pyplot as plt
from functools import lru_cache
from typing import List, Callable, Tuple


def fact_recursive(n: int) -> int:
    """
    Вычисление факториал числа рекурсивным методом.
    
    Args:
        n (int): Число для вычисления факториала (n >= 0)
        
    Returns:
        int: Значение n!
    """
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


@lru_cache(maxsize=None)
def fact_recursive_cached(n: int) -> int:
    """
    Вычисление факториал числа рекурсивным методом с мемоизацией.
    
    Args:
        n (int): Число для вычисления факториала (n >= 0)
        
    Returns:
        int: Значение n!
    """
    if n == 0:
        return 1
    return n * fact_recursive_cached(n - 1)


def fact_iterative(n: int) -> int:
    """
    Вычисление факториал числа итеративным методом (через цикл).
    
    Args:
        n (int): Число для вычисления факториала (n >= 0)
        
    Returns:
        int: Значение n!
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def benchmark(func: Callable[[int], int], n: int, number: int = 1000, repeat: int = 5) -> float:
    """
    Замер времени выполнения функции для заданного n.
    
    Args:
        func: Функция для тестирования
        n: Аргумент функции
        number: Количество вызовов в одном прогоне
        repeat: Количество повторений для усреднения
        
    Returns:
        float: Минимальное время выполнения в секундах на один вызов
    """
    setup_str = f"from __main__ import {func.__name__}"
    stmt = f"{func.__name__}({n})"
    
    times = timeit.repeat(stmt=stmt, setup=setup_str, repeat=repeat, number=number)
    
    return min(times) / number


def run_all_comparisons() -> Tuple[List[int], List[float], List[float], List[float]]:
    """
    Запуск сравнения всех трех методов.
    
    Returns:
        Tuple с test_data и результатами для всех методов
    """
    test_data = list(range(10, 301, 10))
    
    results_recursive: List[float] = []
    results_recursive_cached: List[float] = []
    results_iterative: List[float] = []
    
    
    for i, n in enumerate(test_data):
        if i > 0:
            fact_recursive_cached.cache_clear()
        
        time_recursive = benchmark(fact_recursive, n, number=1000, repeat=5)
        results_recursive.append(time_recursive)
        
        time_cached = benchmark(fact_recursive_cached, n, number=1000, repeat=5)
        results_recursive_cached.append(time_cached)
        
        time_iterative = benchmark(fact_iterative, n, number=1000, repeat=5)
        results_iterative.append(time_iterative)
        
        if n % 50 == 0:
            print(f"n={n:3d}: "
                  f"Рекурсивный={time_recursive:.2e} с, "
                  f"Рекурсивный(кэш)={time_cached:.2e} с, "
                  f"Итеративный={time_iterative:.2e} с")
    
    return test_data, results_recursive, results_recursive_cached, results_iterative


def print_statistics(test_data: List[int], 
                     results_recursive: List[float],
                     results_recursive_cached: List[float],
                     results_iterative: List[float]) -> None:
    """
    Вывод статистики сравнения всех методов.
    """

    print("Сравнение всех методов:")

    
    key_points = [50, 100, 200, 300]
    
    for n in key_points:
        if n <= 300:
            idx = test_data.index(n)
            ratio_no_cache = results_recursive[idx] / results_iterative[idx] if results_iterative[idx] > 0 else 0
            
            print(f"\nn = {n}:")
            print(f"  Рекурсивный (без кэша): {results_recursive[idx]:.2e} с")
            print(f"  Рекурсивный (с кэшем):  {results_recursive_cached[idx]:.2e} с")
            print(f"  Итеративный:           {results_iterative[idx]:.2e} с")


def save_recursive_vs_iterative_plot(test_data: List[int],
                                     results_recursive: List[float],
                                     results_iterative: List[float]) -> None:
    """
    Сохранение графика сравнения рекурсивного и итеративного методов.
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(test_data, results_recursive, 'g-', label='Рекурсивный', linewidth=2)
    plt.plot(test_data, results_iterative, 'b-', label='Итеративный', linewidth=2)
    
    plt.xlabel('n ', fontsize=12)
    plt.ylabel('Время (сек)', fontsize=12)
    plt.title('Сравнение рекурсивного и итеративного факториала', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    plt.savefig('recursive_vs_iterative_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()


def main() -> None:
    """
    Функция для запуска сравнения и сохранения графика.
    """
    print("Вычисление факториала:")
    
    test_data, results_recursive, results_recursive_cached, results_iterative = run_all_comparisons()
    
    print_statistics(test_data, results_recursive, results_recursive_cached, results_iterative)
    
    save_recursive_vs_iterative_plot(test_data, results_recursive, results_iterative)


if __name__ == "__main__":
    main()