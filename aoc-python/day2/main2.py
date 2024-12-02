def is_legal_and_increasing(prev_val, val):
    difference = val-prev_val

    if difference > 0 and difference <= 3:
        return True, True
    if difference < 0 and difference >= -3:
        return True, False
    
    return False, False


def is_legal(arr):
    if len(arr) == 1:
        return True
    
    is_legal, is_required_increasing = is_legal_and_increasing(arr[0], arr[1])

    if not is_legal:
        return False
    
    for idx, val in enumerate(arr):
        if idx < 2:
            continue
        is_legal, is_increasing = is_legal_and_increasing(arr[idx-1], arr[idx])
        if is_required_increasing != is_increasing:
            return False
        if not is_legal:
            return False
        
    return True

f = open('input.txt', 'r')

arr3d = []

for line in f:
    arr = [int(val) for val in line.split()]
    
    arr3d.append(arr)

legal = 0

for arr in arr3d:
    if is_legal(arr):
        legal +=1
    else:
        # brute force the checks
        any_is_legal = False
        for idx, val in enumerate(arr):
            sliced_arr = arr.copy()
            del sliced_arr[idx]
            if is_legal(sliced_arr):
                any_is_legal = True
                break
        
        if any_is_legal:
            legal +=1
