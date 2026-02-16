# Лабораторная работа №6
Выполнила: Николаева Александра</p>
Задание: Сравните время работы двух реализаций функции построения бинарного дерева:<ul>
<li>рекурсивной </li>
<li>нерекурсивной.</li></ul></p>
Требуется:<ol>
<li>Реализовать внутри одного файла две функции:
<ul><li>build_tree_recursive(data)
<li>build_tree_iterative(data)</li></ul>
<li>Сравнить их время работы с помощью timeit.
<li>Построить график (ось X — высота дерева, ось Y — время построения дерева).
<li>Сделать выводы о сравнении двух подходов.</li></ol></p>
Дерево должно обладать следующими свойствами:
<ul><li>В корне дерева (root) находится число, которое задает пользователь (индивидуально для студента).</li>
<li>Высота дерева (height) задается пользователем (индивидуально для студента).</li>
<li>Левый (left leaf) и правый потомок (right leaf) вычисляется с использованием алгоритмов Root = 12; height = 4, left_leaf = root^3, right_leaf = (root*2)-1</li></ul></p>
Код программы:</p>
<img width="800" height="1199" alt="image" src="https://github.com/user-attachments/assets/aed505d5-2372-4fa1-9c7e-860912c4e33d" />
<img width="800" height="1129" alt="image" src="https://github.com/user-attachments/assets/1ded9c03-7aca-4c91-8a2b-e8766d3639d2" /></p>
Вывод:</p>
<img width="600" height="342" alt="image" src="https://github.com/user-attachments/assets/45320fbd-d513-4d4a-8140-ce065a114ade" /></p>
График:</p>
<img width="600" height="753" alt="image" src="https://github.com/user-attachments/assets/14305d32-6f0e-4c20-b0e5-9b49bca8faf8" /></p>

