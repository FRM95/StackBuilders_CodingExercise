# Count words in a title
def counting_words(text:str):
    words, l, r = 0, 0, 0
    while r < len(text):
        if text[r].isalnum(): 
            words += 1
            l = r + 1
            while l < len(text):
                if text[l] == " ":
                    break
                l += 1
            r = l + 1
        else: 
            r += 1
    return words

# Apply filter 1 defined in filter operations
# Filter all previous entries with more than five words in the title ordered by the number of comments first.
def apply_filter_1(array: list) -> list|str:
    try:
        l_filtered = list(filter(lambda x: counting_words(x.get('title')) > 5, array))
        l_sorted = sorted(l_filtered, key = lambda x: x.get('comments'), reverse=True)
    except Exception as e:
        return f'Unknown exception {e}'
    else:
        return l_sorted

# Apply filter 2 defined in filter operations
# Filter all previous entries with less than or equal to five words in the title ordered by points.
def apply_filter_2(array: list) -> list|str:
    try:
        l_filtered = list(filter(lambda x: counting_words(x.get('title')) <= 5, array))
        l_sorted = sorted(l_filtered, key = lambda x: x.get('score'), reverse=True)
    except Exception as e:
        return f'Unknown exception {e}'
    else:
        return l_sorted

# Select what filter to apply
def applyFilter(array: list, option: int) -> list|str:
    if not isinstance(array, list):
        return 'Wrong parameter type array, must be list'
    elif isinstance(array, list) and len(array) == 0:
        return 'Wrong array value, array can not be empty'
    elif not isinstance(option, int):
        return 'Wrong parameter type option, must be int'
    try:
        if option == 1:
            filtered_array = apply_filter_1(array)
        elif option == 2:
            filtered_array = apply_filter_2(array)
    except Exception as e:
        return f'Unknown exception {e}'
    else:
        return filtered_array