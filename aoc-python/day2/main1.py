


# gives increasing or decreasing value
def is_legal_and_increasing(prev_val, val):
    difference = val-prev_val

    if difference > 0 and difference <= 3:
        return True, True
    if difference < 0 and difference >= -3:
        return True, False
    
    return False, False
    
    
f = open('input.txt', 'r')

arr3d = []

for line in f:
    arr = [int(val) for val in line.split()]
    
    arr3d.append(arr)

legal = 0

for arr in arr3d:
    required_is_increasing = None
    is_all_legal = True
    for idx, val in enumerate(arr):
        if idx == 0:
            continue
        prev_val = arr[idx-1]
        if idx == 1 and val - prev_val > 0:
            required_is_increasing = True
        if idx == 1 and val - prev_val < 0:
            required_is_increasing = False
        if idx == 1 and val - prev_val == 0:
            is_all_legal = False
            break
            
        is_legal, is_increasing = is_legal_and_increasing(prev_val,val)

        if required_is_increasing == is_increasing and is_legal:
            continue
        else:
            is_all_legal = False
            break
    if is_all_legal:
        legal += 1


print(legal)
            
