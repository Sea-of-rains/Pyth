import sys
import logging
import functools
import io
import requests
import json
import math
import unittest
from unittest.mock import patch, Mock
from typing import Any, Callable, Union, Optional, TextIO, List, Dict

def logger(func: Optional[Callable] = None, *, handle=sys.stdout):
    """
    Параметризуемый декоратор для логирования вызовов функций.
    
    Args:
        func: Декорируемая функция
        handle: Куда производить логирование (sys.stdout, файловый объект, logging.Logger)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            is_logger = isinstance(handle, logging.Logger)
            
            def log(level, message):
                if is_logger:
                    if level == "INFO":
                        handle.info(message)
                    elif level == "ERROR":
                        handle.error(message)
                    elif level == "WARNING":
                        handle.warning(message)
                    elif level == "CRITICAL":
                        handle.critical(message)
                else:
                    handle.write(f"{level}: {message}\n")
                    if hasattr(handle, 'flush'):
                        handle.flush()
            
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            
            log("INFO", f"Вызов {func.__name__}({signature})")
            
            try:
                result = func(*args, **kwargs)
                log("INFO", f"{func.__name__} вернула {result!r}")
                return result
            except Exception as e:
                log("ERROR", f"Исключение в {func.__name__}: {type(e).__name__}: {e}")
                raise
        
        return wrapper
    
    if func is not None:
        return decorator(func)
    
    return decorator


def get_currencies(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Dict[str, float]:
    """
    Получает курсы валют с API ЦБ РФ.
    
    Args:
        currency_codes: Список кодов валют
        url: URL API ЦБ РФ
    
    Returns:
        Словарь вида {"USD": 93.25, "EUR": 101.7}
    
    Raises:
        ConnectionError: Если API недоступен
        ValueError: Если получен некорректный JSON
        KeyError: Если отсутствует ключ "Valute" или запрошенная валюта
        TypeError: Если курс валюты имеет неверный тип
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            raise ValueError("Некорректный JSON ответ от API")
        
        if "Valute" not in data:
            raise KeyError("В ответе API отсутствует ключ 'Valute'")
        
        valutes = data["Valute"]
        result = {}
        
        for code in currency_codes:
            if code not in valutes:
                raise KeyError(f"Валюта {code} отсутствует в данных")
            
            currency_data = valutes[code]
            if "Value" not in currency_data:
                raise KeyError(f"Для валюты {code} отсутствует поле Value")
            
            value = currency_data["Value"]
            if not isinstance(value, (int, float)):
                raise TypeError(f"Курс валюты {code} имеет неверный тип: {type(value).__name__}")
            
            result[code] = float(value)
        
        return result
        
    except requests.RequestException as e:
        raise ConnectionError(f"API недоступен: {e}")


@logger
def get_currencies_stdout(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Dict[str, float]:
    return get_currencies(currency_codes, url)


stream = io.StringIO()
@logger(handle=stream)
def get_currencies_stream(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Dict[str, float]:
    return get_currencies(currency_codes, url)


file_logger = logging.getLogger("currency_file")
file_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("currency_log.txt", encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

file_logger.addHandler(file_handler)

@logger(handle=file_logger)
def get_currencies_file(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Dict[str, float]:
    return get_currencies(currency_codes, url)


def solve_quadratic(a, b, c):
    """
    Решает квадратное уравнение ax^2 + bx + c = 0
    """
    if not all(isinstance(x, (int, float)) for x in [a, b, c]):
        raise TypeError("Все коэффициенты должны быть числами")
    
    if a == 0 and b == 0:
        if c == 0:
            return "Бесконечное множество решений"
        else:
            raise ValueError("Нет решений (противоречивое уравнение)")
    
    if a == 0:
        x = -c / b
        return (x,)
    
    discriminant = b**2 - 4*a*c
    
    if discriminant < 0:
        return "WARNING: Дискриминант отрицательный, нет действительных корней"
    elif discriminant == 0:
        x = -b / (2*a)
        return (x,)
    else:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return (x1, x2)


@logger
def solve_quadratic_logged(a, b, c):
    return solve_quadratic(a, b, c)


def demonstrate_quadratic():
    print("Демонстрация solve_quadratic")
    
    print("\n1. Два корня:")
    result = solve_quadratic_logged(1, -3, 2)
    print(f"Результат: {result}")
    
    print("\n2. Дискриминант < 0:")
    result = solve_quadratic_logged(1, 1, 1)
    print(f"Результат: {result}")
    
    print("\n3. Некорректные данные:")
    try:
        solve_quadratic_logged("abc", 2, 1)
    except TypeError as e:
        print(f"Поймано исключение: {e}")
    
    print("\n4. Невозможная ситуация:")
    try:
        solve_quadratic_logged(0, 0, 5)
    except ValueError as e:
        print(f"Поймано исключение: {e}")


def demonstrate_currencies():
    print("Демонстрация get_currencies")
    
    try:
        result = get_currencies_stdout(['USD', 'EUR'])
        print(f"Курсы валют: {result}")
    except Exception as e:
        print(f"Ошибка при получении курсов: {e}")
    
    print("Демонстрация файлового логирования")
    try:
        result = get_currencies_file(['USD', 'EUR'])
        print(f"Курсы валют: {result}")
        print("Логи сохранены в файл currency_log.txt")
    except Exception as e:
        print(f"Ошибка: {e}")


class TestGetCurrencies(unittest.TestCase):
    
    def setUp(self):
        self.valid_response = {
            "Valute": {
                "USD": {"Value": 93.25},
                "EUR": {"Value": 101.7}
            }
        }
    
    @patch('requests.get')
    def test_correct_return(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.valid_response
        mock_get.return_value = mock_response
        
        result = get_currencies(['USD', 'EUR'])
        self.assertEqual(result, {"USD": 93.25, "EUR": 101.7})
    
    @patch('requests.get')
    def test_nonexistent_currency(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.valid_response
        mock_get.return_value = mock_response
        
        with self.assertRaises(KeyError) as context:
            get_currencies(['GBP'])
        
        self.assertIn("Валюта GBP отсутствует", str(context.exception))
    
    @patch('requests.get')
    def test_connection_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Connection failed")
        
        with self.assertRaises(ConnectionError):
            get_currencies(['USD'])
    
    @patch('requests.get')
    def test_invalid_json(self, mock_get):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError):
            get_currencies(['USD'])
    
    @patch('requests.get')
    def test_missing_valute_key(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        with self.assertRaises(KeyError) as context:
            get_currencies(['USD'])
        
        self.assertIn("отсутствует ключ 'Valute'", str(context.exception))
    
    @patch('requests.get')
    def test_type_error(self, mock_get):
        invalid_response = {
            "Valute": {
                "USD": {"Value": "не число"}
            }
        }
        mock_response = Mock()
        mock_response.json.return_value = invalid_response
        mock_get.return_value = mock_response
        
        with self.assertRaises(TypeError):
            get_currencies(['USD'])


class TestLoggerDecorator(unittest.TestCase):
    
    def setUp(self):
        self.stream = io.StringIO()
        
        @logger(handle=self.stream)
        def test_function(x, y=2):
            return x * y
        
        self.test_function = test_function
        
        @logger(handle=self.stream)
        def error_function():
            raise ValueError("Тестовая ошибка")
        
        self.error_function = error_function
    
    def test_success_logging(self):
        result = self.test_function(3, y=4)
        
        self.assertEqual(result, 12)
        
        logs = self.stream.getvalue()
        
        self.assertIn("INFO: Вызов test_function(3, y=4)", logs)
        
        self.assertIn("INFO: test_function вернула 12", logs)
    
    def test_error_logging(self):
        with self.assertRaises(ValueError):
            self.error_function()
        
        logs = self.stream.getvalue()
        
        self.assertIn("ERROR: Исключение в error_function: ValueError: Тестовая ошибка", logs)
        self.assertIn("INFO: Вызов error_function()", logs)


class TestStreamWrite(unittest.TestCase):
    
    def setUp(self):
        self.stream = io.StringIO()
        
        @logger(handle=self.stream)
        def wrapped():
            return get_currencies(['USD'], url="https://invalid")
        
        self.wrapped = wrapped
    
    def test_logging_error(self):
        with self.assertRaises(ConnectionError):
            self.wrapped()
        
        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)


class TestFileLogging(unittest.TestCase):
    
    def test_file_logger_creation(self):
        self.assertIsNotNone(file_logger)
        self.assertEqual(len(file_logger.handlers), 1)
        self.assertIsInstance(file_logger.handlers[0], logging.FileHandler)


class TestSolveQuadratic(unittest.TestCase):
    
    def test_two_roots(self):
        result = solve_quadratic(1, -3, 2)
        self.assertEqual(result, (2.0, 1.0))
    
    def test_one_root(self):
        result = solve_quadratic(1, -2, 1)
        self.assertEqual(result, (1.0,))
    
    def test_negative_discriminant(self):
        result = solve_quadratic(1, 1, 1)
        self.assertEqual(result, "WARNING: Дискриминант отрицательный, нет действительных корней")
    
    def test_linear_equation(self):
        result = solve_quadratic(0, 2, -4)
        self.assertEqual(result, (2.0,))
    
    def test_invalid_data(self):
        with self.assertRaises(TypeError):
            solve_quadratic("abc", 2, 1)
    
    def test_impossible_situation(self):
        with self.assertRaises(ValueError):
            solve_quadratic(0, 0, 5)


if __name__ == '__main__':

    print("ЗАПУСК ДЕМОНСТРАЦИИ")
   
    demonstrate_quadratic()
    
    demonstrate_currencies()
    
    print("ЗАПУСК ТЕСТОВ")
    
    unittest.main(argv=[''], verbosity=2, exit=False)