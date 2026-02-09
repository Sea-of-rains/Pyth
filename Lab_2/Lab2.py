from typing import List, Union, Optional, Tuple


def guess_number(target: int, lst: List[int], search_type: str = 'seq') -> Tuple[Optional[int], Optional[int]]:
    """
    Функция для поиска числа в списке с использованием указанного алгоритма.
    
    Args:
        target: Искомое число
        lst: Список чисел для поиска (может быть неотсортированным)
        search_type: Тип поиска - 'seq' для последовательного, 'bin' для бинарного
    
    Returns:
        Кортеж из двух элементов: (найденное_число, количество_сравнений)
        Если число не найдено, возвращает (None, количество_сравнений)
    
    Raises:
        ValueError: Если передан неподдерживаемый тип поиска
    """
    comparisons = 0
    
    if search_type == 'seq':
        # Последовательный поиск
        for num in lst:
            comparisons += 1
            if num == target:
                return (num, comparisons)
        return (None, comparisons)
    
    elif search_type == 'bin':
        # Бинарный поиск требует отсортированного списка
        sorted_lst = sorted(lst)
        left = 0
        right = len(sorted_lst) - 1
        
        while left <= right:
            comparisons += 1
            mid = (left + right) // 2
            
            if sorted_lst[mid] == target:
                return (sorted_lst[mid], comparisons)
            elif sorted_lst[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return (None, comparisons)
    
    else:
        raise ValueError(f"Неподдерживаемый тип поиска: {search_type}. "
                        f"Используйте 'seq' или 'bin'.")


def input_range_from_keyboard() -> tuple[int, int, int]:
    """
    Вспомогательная функция для ввода данных с клавиатуры.
    
    Returns:
        Кортеж из трех элементов: (target, start_range, end_range)
    """
    print("Ввод данных")
    
    target = int(input('Искомое число: '))
    start_range = int(input('Начало диапазона: '))
    end_range = int(input('Конец диапазона: '))
    
    # Проверка корректности диапазона
    if start_range > end_range:
        start_range, end_range = end_range, start_range
    
    return target, start_range, end_range


def main():
    """
    Основная функция программы.
    Формирует список по диапазону, введенному с клавиатуры,
    затем выполняет поиск числа и выводит результаты.
    """
    print("'Угадай число'")
    
    # Автоматическое формирование списка по диапазону
    target, start_range, end_range = input_range_from_keyboard()
    lst = list(range(start_range, end_range + 1))
    
    print(f"\nСформирован список: {lst}")
    
    print("\nАлгоритм поиска:")
    print("1 - Последовательный")
    print("2 - Бинарный")
    
    search_choice = input("? ")
    search_type = 'seq' if search_choice == '1' else 'bin'
    
    if search_type == 'bin' and lst != sorted(lst):
        lst = sorted(lst)
        
    
    # Выполняем поиск
    try:
        found_number, comparisons = guess_number(target, lst, search_type)
        
        print("\nРЕЗУЛЬТАТЫ ПОИСКА:")
        print(f"Алгоритм поиска - {'Последовательный' if search_type == 'seq' else 'Бинарный'}")
        print(f"Количество сравнений: {comparisons}")
        
        if found_number is not None:
            print(f"Число {found_number} найдено!")
            
            # Для последовательного поиска выводим позицию
            if search_type == 'seq':
                position = lst.index(found_number) + 1
                print(f"Позиция в списке: {position}")
            
                
        else:
            print(f"Число {target} НЕ найдено в списке!")
        
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()
    