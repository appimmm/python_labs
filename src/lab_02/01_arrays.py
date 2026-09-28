def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """Возвращает кортеж (мин, макс). При пустом списке вызывает ValueError."""
    if not nums:
        raise ValueError('пустой список')
    
    min_val = nums[0]
    max_val = nums[0]
    for num in nums:
        if num < min_val:
            min_val = num
        if num > max_val:
            max_val = num           
    return (min_val, max_val)


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """Возвращает отсортированный по возрастанию список уникальных значений."""
    if not nums:
        return []
        
    res_list = []
    for item in nums:
        if item not in res_list:
            res_list.append(item)

    for i in range(len(res_list)):
        for j in range(0, len(res_list) - i - 1):
            if res_list[j] > res_list[j + 1]:
                # Меняем элементы местами
                res_list[j], res_list[j + 1] = res_list[j + 1], res_list[j]               
    return res_list


def flatten(mat: list[list | tuple]) -> list:
    """Делает из списка списков или кортежей плоский одномерный список."""
    flat_list = []
    for el in mat:
        if not isinstance(el, (list, tuple)):
            raise TypeError("Элемент не является списком или кортежем")
        
        for element in el:
            flat_list.append(element)            
    return flat_list




print("min_max")
print(min_max([3, -1, 5, 5, 0]))                 
print(min_max([42]))                             
print(min_max([-5, -2, -9]))
try:
    print(min_max([]))
except ValueError as e:
    print(f"ValueError:{e}")
except TypeError as e:
    print(f"TypeError: {e}")
print(min_max([1.5, 2, 2.0, -3.1]))              

print("\nunique_sorted")
print(unique_sorted([3, 1, 2, 1, 3]))      
print(unique_sorted([]))    
print(unique_sorted([-1, -1, 0, 2, 2]))    
print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))

print("\nflatten")
print(flatten([[1, 2], [3, 4]]))                 
print(flatten([[1, 2], (3, 4, 5)]))              
print(flatten([[1], [], [2, 3]]))
try:
    print(flatten([[1, 2], "ab"]))
except TypeError as e:
    print(f"TypeError: {e}")
except ValueError as e:
    print(f"ValueError: {e}")