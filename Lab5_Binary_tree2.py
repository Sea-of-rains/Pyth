from collections import deque, namedtuple, defaultdict, OrderedDict
from typing import Dict, Optional, Callable

# Определение структуры узла с помощью namedtuple
TreeNode = namedtuple('TreeNode', ['value', 'left', 'right'])

def gen_bin_tree(height: int = 4, 
                 root: int = 12, 
                 left_branch: Callable[[int], int] = lambda x: x ** 3,
                 right_branch: Callable[[int], int] = lambda x: (x * 2) - 1) -> Dict:
    """
    Генерация бинарного дерева нерекурсивным способом.
    
    Args:
        height: Высота дерева
        root: Значение корневого узла
        left_branch: Функция для вычисления левого потомка
        right_branch: Функция для вычисления правого потомка
    
    Returns:
        Словарь, представляющий бинарное дерево
    """
    if height <= 0:
        return {}
    
    # Используем стек для нерекурсивного обхода
    stack = []
    tree_dict = {}
    
    # Инициализируем корень
    stack.append(("root", root, 1))  # (путь, значение, текущая высота)
    
    while stack:
        path, value, current_height = stack.pop()
        
        # Добавляем узел в словарь
        tree_dict[path] = value
        
        # Если достигли максимальной высоты, не добавляем потомков
        if current_height >= height:
            continue
        
        # Вычисляем значения потомков
        left_value = left_branch(value)
        right_value = right_branch(value)
        
        # Добавляем правого потомка первым (так как используем стек - LIFO)
        right_path = f"{path}.right"
        stack.append((right_path, right_value, current_height + 1))
        
        # Добавляем левого потомка
        left_path = f"{path}.left"
        stack.append((left_path, left_value, current_height + 1))
    
    return tree_dict


def gen_bin_tree_collections(height: int = 4, 
                            root: int = 12,
                            left_branch: Callable[[int], int] = lambda x: x ** 3,
                            right_branch: Callable[[int], int] = lambda x: (x * 2) - 1):
    """
    Генерация бинарного дерева с использованием различных структур из collections.
    """    
    # 1. Использование deque для обхода дерева (BFS)
    print("\n Использование deque для обхода в ширину (BFS):")
    
    if height <= 0:
        return []
    
    bfs_result = []
    queue = deque()
    queue.append(("root", root, 1))
    
    while queue:
        path, value, current_height = queue.popleft()
        bfs_result.append((path, value))
        
        if current_height < height:
            left_value = left_branch(value)
            right_value = right_branch(value)
            
            left_path = f"{path}.left"
            right_path = f"{path}.right"
            
            queue.append((left_path, left_value, current_height + 1))
            queue.append((right_path, right_value, current_height + 1))
    
    print(f"   Обход в ширину: {bfs_result}")
    print(f"   Количество узлов: {len(bfs_result)}")
    
    # 2. Использование namedtuple для представления узлов
    print("\n Использование namedtuple:")
    
    def build_tree_namedtuple(value: int, current_height: int, max_height: int) -> Optional[TreeNode]:
        """Рекурсивное построение дерева с использованием namedtuple"""
        if current_height > max_height:
            return None
        
        left_child = None
        right_child = None
        
        if current_height < max_height:
            left_child = build_tree_namedtuple(left_branch(value), current_height + 1, max_height)
            right_child = build_tree_namedtuple(right_branch(value), current_height + 1, max_height)
        
        return TreeNode(value=value, left=left_child, right=right_child)
    
    namedtree = build_tree_namedtuple(root, 1, height)
    print(f"   Корень дерева: {namedtree.value if namedtree else 'None'}")
    print(f"   Левый потомок корня: {namedtree.left.value if namedtree and namedtree.left else 'None'}")
    print(f"   Правый потомок корня: {namedtree.right.value if namedtree and namedtree.right else 'None'}")
    
    # 3. Использование defaultdict для хранения дерева по уровням
    print("\n Использование defaultdict:")
    
    level_dict = defaultdict(list)
    stack = [(root, "root", 1)]
    
    while stack:
        value, path, current_height = stack.pop()
        level_dict[current_height].append((path, value))
        
        if current_height < height:
            left_value = left_branch(value)
            right_value = right_branch(value)
            
            left_path = f"{path}.left"
            right_path = f"{path}.right"
            
            stack.append((right_value, right_path, current_height + 1))
            stack.append((left_value, left_path, current_height + 1))
    
    print("   Дерево по уровням:")
    for level in sorted(level_dict.keys()):
        nodes = level_dict[level]
        print(f"   Уровень {level}: {nodes}")
    
    # 4. Использование OrderedDict для сохранения порядка добавления
    print("\n Использование OrderedDict :")
    
    ordered_tree = OrderedDict()
    queue = deque([("root", root, 1)])
    
    while queue:
        path, value, current_height = queue.popleft()
        ordered_tree[path] = value
        
        if current_height < height:
            left_value = left_branch(value)
            right_value = right_branch(value)
            
            left_path = f"{path}.left"
            right_path = f"{path}.right"
            
            queue.append((left_path, left_value, current_height + 1))
            queue.append((right_path, right_value, current_height + 1))
    
    print(f"   Порядок узлов в OrderedDict: {list(ordered_tree.keys())}")
    
    return {
        'bfs_result': bfs_result,
        'namedtree': namedtree,
        'level_dict': dict(level_dict),
        'ordered_tree': dict(ordered_tree)
    }


def display_tree(tree_dict: Dict, title: str = "Бинарное дерево в виде словаря"):
    """
    Отображение дерева в удобном формате.
    """
    print(f"\n{title}:")
    
    if not tree_dict:
        print("Дерево пустое")
        return
    
    # Сортируем ключи для удобного отображения
    sorted_keys = sorted(tree_dict.keys(), key=lambda x: (len(x), x))
    
    for key in sorted_keys:
        indent = "  " * (key.count('.') + 1)
        print(f"{indent}{key}: {tree_dict[key]}")
    
    print(f"\nОбщее количество узлов: {len(tree_dict)}")
    print(f"Высота дерева: {max(key.count('.') for key in tree_dict.keys()) + 1}")


def main():
    """
    Основная функция для демонстрации работы программы.
    """
    print("Нерекурсивное бинарное дерево")
    
    tree = gen_bin_tree()
    display_tree(tree)
    
    # Исследование других структур
    collections_results = gen_bin_tree_collections()


if __name__ == "__main__":
    main()