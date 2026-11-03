def bubble_sort(nums) -> list:
    """Новый отсортированный список; исходный список не изменяется."""
    nums = list(nums)
    for end in range(len(nums) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                swapped = True
        if not swapped:
            break
    return nums

def insertion_sort(nums) -> list:
    """Новый отсортированный список методом вставок."""
    nums = list(nums)
    for i in range(1, len(nums)):
        value = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > value:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = value
    return nums

def selection_sort(nums) -> list:
    """Новый отсортированный список методом выбора."""
    nums = list(nums)
    for i in range(len(nums) - 1):
        smallest = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[smallest]:
                smallest = j
        nums[i], nums[smallest] = nums[smallest], nums[i]
    return nums
