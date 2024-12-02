def is_legal(prev_val, val):
    difference = val-prev_val

    if difference > 0 and difference <= 3:
        return True
    if difference < 0 and difference >= -3:
        return True
    
    return False


# either returns True, or the index pair where it was an illegal move
def is_arr_legal(arr):
    for idx, val in enumerate(arr):
        if idx == 0:
            continue
        prev_val = arr[idx-1]
            
        if is_legal(prev_val, val):
            continue
        
        return [idx-1, idx]
    
    return True

# care about steps, not care about increase/decrease
for arr in arr3d:
    free_life_used = False
    output = is_arr_legal(arr)
    if output == True:
        legal_arrs.append(
            {
                "arr": arr,
                "used_life" : False,
            } )
    else:
        # try again with valid indices
        arr_
        output = is_arr_legal(arr)
        
    