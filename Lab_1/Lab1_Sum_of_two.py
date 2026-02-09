print("Введите массив целых чисел:")
M = input().split()
num1 = [int(num) for num in M]

print("Введите значение суммы:")
target = int(input(" "))

def sumoftwo(num1, target):
    
    if len(num1) < 2:
        print("Массив содержит меньше 2х элементов")
        return []
    
    indexed_num1 = [(num, i) for i, num in enumerate(num1)]
    indexed_num1.sort(key=lambda x: x[0])
    left, right = 0, len(indexed_num1) - 1
    result = [] 
    
    while left < right:
        current_sum = indexed_num1[left][0] + indexed_num1[right][0]
        
        if current_sum == target:
            idx1, idx2 = indexed_num1[left][1], indexed_num1[right][1]
            
            pair = [min(idx1, idx2), max(idx1, idx2)]
            
            if not result:
                result = pair
            elif pair[0] < result[0]:  
                result = pair
            elif pair[0] == result[0] and pair[1] < result[1]:  
                result = pair
            
            left += 1
            right -= 1
            
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return result if result else []

result = sumoftwo(num1, target)

if result:
    print(f"Ответ: {result}")
else:
    print("В введённом массиве нет такой пары чисел, которая в сумме даст target")
    