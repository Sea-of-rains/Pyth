import unittest
from main import guess_number


class TestGuessNumber(unittest.TestCase):
    """Тесты для функции guess_number"""
    
    def test_sequential_search_found(self):
        """Тест последовательного поиска (число найдено)"""
        found_number, comparisons = guess_number(5, [1, 2, 3, 4, 5, 6, 7], 'seq')
        self.assertEqual(found_number, 5)
        self.assertEqual(comparisons, 5)
    
    def test_sequential_search_not_found(self):
        """Тест последовательного поиска (число не найдено)"""
        found_number, comparisons = guess_number(10, [1, 2, 3, 4, 5], 'seq')
        self.assertIsNone(found_number)
        self.assertEqual(comparisons, 5)
    
    def test_binary_search_found(self):
        """Тест бинарного поиска (число найдено)"""
        found_number, comparisons = guess_number(5, [1, 2, 3, 4, 5, 6, 7], 'bin')
        self.assertEqual(found_number, 5)
        self.assertEqual(comparisons, 3)
    
    def test_binary_search_not_found(self):
        """Тест бинарного поиска (число не найдено)"""
        found_number, comparisons = guess_number(10, [1, 2, 3, 4, 5], 'bin')
        self.assertIsNone(found_number)
        self.assertEqual(comparisons, 3)
    
    def test_binary_search_unsorted_list(self):
        """Тест бинарного поиска с неотсортированным списком"""
        found_number, comparisons = guess_number(5, [7, 3, 1, 5, 2, 4, 6], 'bin')
        self.assertEqual(found_number, 5)
        self.assertEqual(comparisons, 3)
    
    def test_single_element_found(self):
        """Тест поиска в списке из одного элемента"""
        found_number, comparisons = guess_number(1, [1], 'seq')
        self.assertEqual(found_number, 1)
        self.assertEqual(comparisons, 1)
        
        found_number, comparisons = guess_number(1, [1], 'bin')
        self.assertEqual(found_number, 1)
        self.assertEqual(comparisons, 1)
    
    def test_empty_list(self):
        """Тест поиска в пустом списке"""
        found_number, comparisons = guess_number(1, [], 'seq')
        self.assertIsNone(found_number)
        self.assertEqual(comparisons, 0)
        
        found_number, comparisons = guess_number(1, [], 'bin')
        self.assertIsNone(found_number)
        self.assertEqual(comparisons, 0)
    
    def test_large_list_binary_search(self):
        """Тест бинарного поиска в большом списке"""
        lst = list(range(1, 101))  # 1..100
        found_number, comparisons = guess_number(50, lst, 'bin')
        self.assertEqual(found_number, 50)
        self.assertEqual(comparisons, 6)
    
    def test_invalid_search_type(self):
        """Тест с неправильным типом поиска"""
        with self.assertRaises(ValueError):
            guess_number(5, [1, 2, 3, 4, 5], 'invalid')
    
    def test_duplicate_values_sequential(self):
        """Тест с дублирующимися значениями (только первый будет найден)"""
        found_number, comparisons = guess_number(5, [1, 5, 2, 5, 3, 5], 'seq')
        self.assertEqual(found_number, 5)
        self.assertEqual(comparisons, 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)