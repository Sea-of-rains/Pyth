from typing import List, Union, Optional


def guess_number(target: int, lst: List[int], search_type: str = 'seq') -> List[Union[int, Optional[int]]]:
    """
    Функция для поиска числа в списке с использованием указанного алгоритма.
    
    Args:
        target: Искомое число
        lst: Список чисел для поиска (может быть неотсортированным)
        search_type: Тип поиска - 'seq' для последовательного, 'bin' для бинарного
    
    Returns:
        Список из двух элементов: [найденное_число, количество_сравнений]
        Если число не найдено, возвращает [target, None]
    
    Raises:
        ValueError: Если передан неподдерживаемый тип поиска
    """
    comparisons = 0
    
    if search_type == 'seq':
        # Последовательный поиск
        for num in lst:
            comparisons += 1
            if num == target:
                return [target, comparisons]
        return [target, None]
    
    elif search_type == 'bin':
        # Бинарный поиск требует отсортированного списка
        sorted_lst = sorted(lst)
        left = 0
        right = len(sorted_lst) - 1
        
        while left <= right:
            comparisons += 1
            mid = (left + right) // 2
            
            if sorted_lst[mid] == target:
                return [target, comparisons]
            elif sorted_lst[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return [target, None]
    
    else:
        raise ValueError(f"Неподдерживаемый тип поиска: {search_type}. "
                        f"Используйте 'seq' или 'bin'.")


def input_range_from_keyboard() -> tuple[int, int, int]:
    """
    Вспомогательная функция для ввода данных с клавиатуры.
    
    Returns:
        Кортеж из трех элементов: (target, start_range, end_range)
    """
    print("Ввод данных для 'Угадай число'")
    
    target = int(input('Введите искомое число (target): '))
    start_range = int(input('Введите начало диапазона: '))
    end_range = int(input('Введите конец диапазона: '))
    
    # Проверка корректности диапазона
    if start_range > end_range:
        print("Предупреждение: начало диапазона больше конца. Меняем местами.")
        start_range, end_range = end_range, start_range
    
    return target, start_range, end_range


def input_custom_list() -> List[int]:
    """
    Функция для ручного ввода списка чисел с клавиатуры.
    
    Returns:
        Список введенных пользователем чисел
    """
    print("\nРучной ввод списка чисел")
    print("Вводите числа по одному. Для завершения введите 'stop'")
    
    lst = []
    while True:
        user_input = input(f"Число {len(lst) + 1} (или 'stop' для завершения): ")
        
        if user_input.lower() == 'stop':
            if len(lst) < 2:
                print("Список должен содержать хотя бы 2 числа. Продолжайте ввод.")
                continue
            break
        
        try:
            num = int(user_input)
            if num in lst:
                print(f"Число {num} уже есть в списке. Пропускаем.")
                continue
            lst.append(num)
        except ValueError:
            print("Ошибка! Введите целое число или 'stop'.")
    
    return lst


def main():
    """
    Основная функция программы.
    Предлагается выбрать способ формирования списка,
    затем выполняется поиск числа и вывод результатов.
    """
    print("Угадай число")
    print("Способ формирования списка:")
    print("Автоматически(1)")
    print("Самостоятельно(2)")
    
    choice = input("1 или 2? : ")
    
    if choice == '1':
        # Автоматическое формирование списка по диапазону
        target, start_range, end_range = input_range_from_keyboard()
        lst = list(range(start_range, end_range + 1))
        print(f"\nСписок: {lst}")
        print(f"Длина списка: {len(lst)} эл")
        print(f"Искомое число: {target}")
        
    elif choice == '2':
        # Ручной ввод списка
        lst = input_custom_list()
        print(f"\nСписок: {lst}")
        print(f"Длина списка: {len(lst)} эл")
        
        target = int(input('Искомое число (target): '))
        
    else:
        print("Некорректный выбор. Используется автоматическое формирование.")
        target, start_range, end_range = input_range_from_keyboard()
        lst = list(range(start_range, end_range + 1))
    
    print("\nВыберите алгоритм поиска:")
    print("1 - Последовательный поиск (seq)")
    print("2 - Бинарный поиск (bin)")
    
    search_choice = input("Ваш выбор (1 или 2): ")
    search_type = 'seq' if search_choice == '1' else 'bin'
    
    if search_type == 'bin' and lst != sorted(lst):
        print("\nВнимание: для бинарного поиска список будет отсортирован.")
        print(f"Исходный список: {lst}")
        lst = sorted(lst)
        print(f"Отсортированный список: {lst}")
    
    # Выполняем поиск
    try:
        result = guess_number(target, lst, search_type)
        
        print("РЕЗУЛЬТАТЫ ПОИСКА:")
        print(f"Искомое число: {target}")
        print(f"Алгоритм поиска: {'Последовательный' if search_type == 'seq' else 'Бинарный'}")
        
        if result[1] is not None:
            print(f"Число найдено!")
            print(f"Количество сравнений: {result[1]}")
            
            # Для последовательного поиска выводим позицию
            if search_type == 'seq':
                position = lst.index(target) + 1 if target in lst else None
                if position is not None:
                    print(f"Позиция в списке: {position}")

        else:
            print(f"Число НЕ найдено в списке!")
        
        
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()


import unittest


class TestGuessNumber(unittest.TestCase):
    """Тесты для функции guess_number"""
    
    def test_sequential_search_found(self):
        """Тест последовательного поиска (число найдено)"""
        result = guess_number(5, [1, 2, 3, 4, 5, 6, 7], 'seq')
        self.assertEqual(result, [5, 5])
    
    def test_sequential_search_not_found(self):
        """Тест последовательного поиска (число не найдено)"""
        result = guess_number(10, [1, 2, 3, 4, 5], 'seq')
        self.assertEqual(result, [10, None])
    
    def test_binary_search_found(self):
        """Тест бинарного поиска (число найдено)"""
        result = guess_number(5, [1, 2, 3, 4, 5, 6, 7], 'bin')
        self.assertEqual(result, [5, 3])
    
    def test_binary_search_not_found(self):
        """Тест бинарного поиска (число не найдено)"""
        result = guess_number(10, [1, 2, 3, 4, 5], 'bin')
        self.assertEqual(result, [10, None])
    
    def test_binary_search_unsorted_list(self):
        """Тест бинарного поиска с неотсортированным списком"""
        result = guess_number(5, [7, 3, 1, 5, 2, 4, 6], 'bin')
        self.assertEqual(result, [5, 3])
    
    def test_single_element_found(self):
        """Тест поиска в списке из одного элемента"""
        result = guess_number(1, [1], 'seq')
        self.assertEqual(result, [1, 1])
        
        result = guess_number(1, [1], 'bin')
        self.assertEqual(result, [1, 1])
    
    def test_empty_list(self):
        """Тест поиска в пустом списке"""
        result = guess_number(1, [], 'seq')
        self.assertEqual(result, [1, None])
        
        result = guess_number(1, [], 'bin')
        self.assertEqual(result, [1, None])
    
    def test_large_list_binary_search(self):
        """Тест бинарного поиска в большом списке"""
        lst = list(range(1, 101))  # 1..100
        result = guess_number(50, lst, 'bin')
        self.assertEqual(result, [50, 6])  # 2^6 = 64 > 100
    
    def test_invalid_search_type(self):
        """Тест с неправильным типом поиска"""
        with self.assertRaises(ValueError):
            guess_number(5, [1, 2, 3, 4, 5], 'invalid')
    
    def test_duplicate_values_sequential(self):
        """Тест с дублирующимися значениями (только первый будет найден)"""
        result = guess_number(5, [1, 5, 2, 5, 3, 5], 'seq')
        self.assertEqual(result, [5, 2])


def run_tests():
    """Запуск тестов"""
    print("Запуск тестов...")
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    # Можно запускать либо основную программу, либо тесты
    # Для запуска тестов раскомментируйте следующую строку:
    #  run_tests()
    
    # Для запуска основной программы:
    main()
