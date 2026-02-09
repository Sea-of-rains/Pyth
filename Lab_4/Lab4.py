import timeit
import matplotlib.pyplot as plt
from functools import lru_cache
from typing import List, Callable, Tuple


def fact_recursive(n: int) -> int:
    """
    Вычисление факториала числа рекурсивным методом.
    
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
    Вычисление факториала числа рекурсивным методом с мемоизацией.
    
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
    Вычисление факториала числа итеративным методом (через цикл).
    
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


def get_numbers_from_input() -> List[int]:
    """
    Получение списка чисел для тестирования с клавиатуры.
    
    Returns:
        List[int]: Список чисел для вычисления факториала
    """
    while True:
        try:
            input_str = input("Введите числа для вычисления факториала через пробел: ").strip()
            if not input_str:
                print("Ошибка: введите хотя бы одно число")
                continue
                
            numbers = []
            for num_str in input_str.split():
                try:
                    num = int(num_str)
                    if num < 0:
                        print(f"Внимание: число {num} отрицательное, будет взято по модулю")
                        num = abs(num)
                    numbers.append(num)
                except ValueError:
                    print(f"Ошибка: '{num_str}' не является целым числом, пропускаем")
            
            if not numbers:
                print("Ошибка: не удалось распознать ни одного числа, попробуйте снова")
                continue
                
            numbers = sorted(set(numbers))
            return numbers
            
        except KeyboardInterrupt:
            print("\nВвод прерван. Используются значения по умолчанию.")
            return list(range(10, 101, 10))
        except Exception as e:
            print(f"Произошла ошибка: {e}. Попробуйте снова.")


def run_all_comparisons(test_data: List[int]) -> Tuple[List[int], List[float], List[float], List[float]]:
    """
    Запуск сравнения всех трех методов.
    
    Args:
        test_data: Список чисел для тестирования
        
    Returns:
        Tuple с test_data и результатами для всех методов
    """
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
        
        print(f"n={n:4d}: "
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
    print("\nРезультаты тестирования:")
    
    for idx, n in enumerate(test_data):
        print(f"\nn = {n}:")
        print(f"  Рекурсивный (без кэша): {results_recursive[idx]:.2e} с")
        print(f"  Рекурсивный (с кэшем):  {results_recursive_cached[idx]:.2e} с")
        print(f"  Итеративный:           {results_iterative[idx]:.2e} с")


def save_recursive_vs_iterative_plot(test_data: List[int],
                                     results_recursive: List[float],
                                     results_iterative: List[float]) -> None:
    "Визуализация"
    plt.figure(figsize=(12, 7))
    
    plt.plot(test_data, results_recursive, 'g-', label='Рекурсивный (без кэша)', linewidth=2, marker='o')
    plt.plot(test_data, results_iterative, 'b-', label='Итеративный', linewidth=2, marker='s')
    
    plt.xlabel('n', fontsize=12)
    plt.ylabel('Время (сек)', fontsize=12)
    plt.title('Сравнение рекурсивного и итеративного методов вычисления факториала', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    for i, n in enumerate(test_data):
        if len(test_data) <= 10:
            plt.annotate(f'{results_recursive[i]:.1e}', (n, results_recursive[i]), textcoords="offset points", xytext=(0,10), ha='center',fontsize=8)
            plt.annotate(f'{results_iterative[i]:.1e}', (n, results_iterative[i]), textcoords="offset points", xytext=(0,-15), ha='center',fontsize=8)
    
    plt.savefig('recursive_vs_iterative_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    

def main() -> None:
    """
    Основная функция для запуска сравнения и сохранения графика.
    """
    print("Сравнение методов вычисления факториала")
    
    test_data = get_numbers_from_input()
    
    test_data, results_recursive, results_recursive_cached, results_iterative = run_all_comparisons(test_data)
    
    print_statistics(test_data, results_recursive, results_recursive_cached, results_iterative)
    
    save_recursive_vs_iterative_plot(test_data, results_recursive, results_iterative)
    

if __name__ == "__main__":
    main()