from collections import defaultdict, deque
from typing import Any, Dict, Optional

def gen_bin_tree(root: int = 12, height: int = 4, 
                 left_func: callable = None, right_func: callable = None) -> Dict[str, Any]:
    """
    Рекурсивная генерация бинарного дерева в виде словаря.
    
    Args:
        root: корневой узел
        height: высота дерева
        left_func: функция для вычисления левого потомка (root^3)
        right_func: функция для вычисления правого потомка ((root*2)-1)
    
    Returns:
        Словарь, представляющий бинарное дерево
    """
    # Устанавливаем функции по умолчанию, если они не переданы
    if left_func is None:
        left_func = lambda x: x ** 3
    if right_func is None:
        right_func = lambda x: (x * 2) - 1
    
    def build_tree(node_value: int, current_height: int) -> Optional[Dict[str, Any]]:
        """Рекурсивная функция построения дерева."""
        if current_height <= 0:
            return None
        
        tree = {
            'root': node_value,
            'left': None,
            'right': None
        }
        
        if current_height > 1:
            tree['left'] = build_tree(left_func(node_value), current_height - 1)
            tree['right'] = build_tree(right_func(node_value), current_height - 1)
        
        return tree
    
    return build_tree(root, height)


def print_tree(tree: Dict[str, Any], indent: str = "", prefix: str = "root: ") -> None:
    """Рекурсивно печатает дерево в удобочитаемом формате."""
    if tree is None:
        print(indent + prefix + "None")
        return
    
    print(indent + prefix + str(tree['root']))
    
    if tree['left'] is not None or tree['right'] is not None:
        print_tree(tree['left'], indent + "    ", "left: ")
        print_tree(tree['right'], indent + "    ", "right: ")


def tree_to_dict(tree: Dict[str, Any]) -> Dict[str, Any]:
    """Конвертирует дерево в более компактный словарь ."""
    if tree is None:
        return None
    
    result = {
        'value': tree['root']
    }
    
    if tree['left'] is not None or tree['right'] is not None:
        result['children'] = []
        if tree['left'] is not None:
            result['children'].append(tree_to_dict(tree['left']))
        else:
            result['children'].append(None)
        
        if tree['right'] is not None:
            result['children'].append(tree_to_dict(tree['right']))
        else:
            result['children'].append(None)
    
    return result


# Альтернативные реализации с использованием структур из collections
class TreeNode:
    """Класс узла дерева с использованием defaultdict."""
    def __init__(self, value: int):
        self.value = value
        self.children = defaultdict(lambda: None)  # Используем defaultdict


def gen_bin_tree_collections(root: int = 12, height: int = 4) -> TreeNode:
    """
    Генерирует бинарное дерево с использованием структур из collections.
    
    Args:
        root: значение корневого узла
        height: высота дерева
    
    Returns:
        Корневой узел дерева
    """
    def build_node(node_value: int, current_height: int) -> Optional[TreeNode]:
        if current_height <= 0:
            return None
        
        node = TreeNode(node_value)
        
        if current_height > 1:
            left_value = node_value ** 3
            right_value = (node_value * 2) - 1
            
            node.children['left'] = build_node(left_value, current_height - 1)
            node.children['right'] = build_node(right_value, current_height - 1)
        
        return node
    
    return build_node(root, height)


def print_tree_collections(node: TreeNode, indent: str = "", child_type: str = "root") -> None:
    """Печатает дерево, реализованное через класс TreeNode."""
    if node is None:
        print(indent + child_type + ": None")
        return
    
    print(indent + child_type + ": " + str(node.value))
    
    if node.children['left'] is not None or node.children['right'] is not None:
        print_tree_collections(node.children['left'], indent + "    ", "left")
        print_tree_collections(node.children['right'], indent + "    ", "right")


def tree_with_deque(root: int = 12, height: int = 4) -> Dict[int, list]:
    """
    Реализация дерева с использованием deque для обхода в ширину.
    
    Args:
        root: значение корневого узла
        height: высота дерева
    
    Returns:
        Словарь, где ключи - уровни дерева, значения - списки узлов на уровне
    """
    if height <= 0:
        return {}
    
    result = defaultdict(list)
    queue = deque([(root, 0, "root")])  # (значение, уровень, тип)
    
    while queue:
        value, level, node_type = queue.popleft()
        
        if level >= height:
            break
        
        result[level].append((value, node_type))
        
        if level < height - 1:
            left_value = value ** 3
            right_value = (value * 2) - 1
            
            queue.append((left_value, level + 1, "left"))
            queue.append((right_value, level + 1, "right"))
    
    return dict(result)



if __name__ == "__main__":
    print("Бинарное дерево")
    

    tree = gen_bin_tree()
    
    print("\n Дерево в виде вложенного словаря:")
    print_tree(tree)
    
    print("\n Компактное представление дерева:")
    compact_dict = tree_to_dict(tree)
    print(compact_dict)
    
    
    print("\n Дерево с использованием defaultdict:")
    tree_collections = gen_bin_tree_collections()
    print_tree_collections(tree_collections)
    
    print("\n Дерево с использованием deque:")
    tree_deque = tree_with_deque()
    for level, nodes in tree_deque.items():
        print(f"Уровень {level}: {nodes}")
    
  