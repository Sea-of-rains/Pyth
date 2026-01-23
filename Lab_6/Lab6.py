import timeit
import matplotlib.pyplot as plt
from collections import deque
import sys

# Увеличиваем глубину рекурсии
sys.setrecursionlimit(10000)

class TreeNode:
    """Узел бинарного дерева"""
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def build_tree_recursive(height, root_value=12):
    """Рекурсивное построение дерева"""
    if height == 0:
        return None
    
    node = TreeNode(root_value)
    
    if height > 1:
        left_value = root_value ** 3
        right_value = (root_value * 2) - 1
        
        node.left = build_tree_recursive(height - 1, left_value)
        node.right = build_tree_recursive(height - 1, right_value)
    
    return node

def build_tree_iterative(height, root_value=12):
    """Итеративное построение дерева с использованием очереди"""
    if height == 0:
        return None
    
    root = TreeNode(root_value)
    queue = deque()
    queue.append((root, 1, root_value))
    
    while queue:
        node, current_height, value = queue.popleft()
        
        if current_height < height:
            left_value = value ** 3
            right_value = (value * 2) - 1
            
            node.left = TreeNode(left_value)
            node.right = TreeNode(right_value)
            
            queue.append((node.left, current_height + 1, left_value))
            queue.append((node.right, current_height + 1, right_value))
    
    return root

def main():
    """Основная функция для сравнения производительности и создания графика"""
    heights = list(range(1, 12))
    recursive_times = []
    iterative_times = []
    
    print("Измерение времени построения дерева...")
    print(f"{'Высота':<10} {'Рекурсивная (с)':<20} {'Итеративная (с)':<20}")
    
    for height in heights:
        # Измеряем время рекурсивной версии
        recursive_time = timeit.timeit(
            lambda: build_tree_recursive(height),
            number=10
        ) / 10
        
        # Измеряем время итеративной версии
        iterative_time = timeit.timeit(
            lambda: build_tree_iterative(height),
            number=10
        ) / 10
        
        recursive_times.append(recursive_time)
        iterative_times.append(iterative_time)
        
        print(f"{height:<10} {recursive_time:<20.6f} {iterative_time:<20.6f}")
    
    # Создание графика в линейном масштабе
    plt.figure(figsize=(10, 6))
    
    plt.plot(heights, recursive_times, 'b-o', label='Рекурсивная реализация', linewidth=2, markersize=8)
    plt.plot(heights, iterative_times, 'r-s', label='Итеративная реализация', linewidth=2, markersize=8)
    
    plt.xlabel('Высота дерева', fontsize=12)
    plt.ylabel('Время построения (секунды)', fontsize=12)
    plt.title('Сравнение времени построения бинарного дерева', fontsize=14, fontweight='bold')
    
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    
    plt.tight_layout()
    
    # Сохраняем график в файл
    plt.savefig('tree_build_comparison.png', dpi=300, bbox_inches='tight')
    
    
    # Отображаем график
    plt.show()

if __name__ == "__main__":
    main()