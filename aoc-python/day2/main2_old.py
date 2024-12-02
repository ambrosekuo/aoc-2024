
f = open('input.txt', 'r')

arr3d = []

for line in f:
    arr = [int(val) for val in line.split()]
    
    arr3d.append(arr)

legal_arrs = []


def is_legal_and_increasing(prev_val, val):
    difference = val-prev_val

    if difference > 0 and difference <= 3:
        return True, True
    if difference < 0 and difference >= -3:
        return True, False
    
    return False, False

legal = 0
for arr in arr3d:
    required_is_increasing = None
    is_all_legal = True
    extra_life_used = False
    prev_val = None

    for idx, val in enumerate(arr):
        if idx == 0:
            prev_val = val
            continue
            
        is_legal, is_increasing = is_legal_and_increasing(prev_val,val)

        if idx == 1 and len(arr) > 3:
            if not is_legal:
                extra_life_used = True
                next_val =  arr[idx+1]
                is_legal_1, is_increasing_1 = is_legal_and_increasing(prev_val, next_val)
                is_legal_2, is_increasing_2 = is_legal_and_increasing(val, next_val)

                # doesn't matter, we're done
                if len(arr) == 3 and (is_legal_1 or is_legal_2):
                    break
                
                # if both legal, # 1 5 2 case where either 1 or 5 can be removed, depends on the 4th index
                if is_legal_1 and is_legal_2:
                    if len(arr) > 3:
                        next_next_val = arr[idx+2]
                        is_legal_3, is_increasing_3 = is_legal_and_increasing(next_val, next_next_val)

                        if not is_legal_3:
                            is_all_legal = False
                            break
                        
                        if is_increasing_3 == is_increasing_1: # skip this one
                            required_is_increasing = is_increasing_1
                            continue
                        else: # keep this one, last one was the wrong one
                            required_is_increasing = is_increasing_2
                            prev_val = val
                            continue
                elif is_legal_1:
                    required_is_increasing = is_increasing_1
                    continue
                elif is_legal_2:
                    required_is_increasing = is_increasing_2
                    prev_val = val
                    continue
                else:
                    is_all_legal = False
                    break
            else:
                required_is_increasing = is_increasing

        if required_is_increasing == is_increasing and is_legal:
            prev_val = val
            continue
        else: 
            if extra_life_used:
                is_all_legal = False
                break

            extra_life_used = True

            # crazy edge case, if we have to check a general amount of times, we're fucked. thank god its once
            if not is_legal and idx == 2 and len(arr) > 3: # possible to remove the first one here 
                # let's say we think the bad case is the first one, we change our "direction rule"
                # let's check if the next one is following this or even legal
                is_legal_1, is_increasing_1 = is_legal_and_increasing(prev_val, arr[idx+1])
                is_legal_2, is_increasing_2 = is_legal_and_increasing(val, arr[idx+1])
                if not is_legal_1: # if previous not legal, we have to remove it
                    # check if current val is valid with last one
                    is_legal_3, is_increasing_3 = is_legal_and_increasing(arr[idx-2], val)
                    if not is_legal_3: # we're done
                        is_all_legal = False
                        break
                    required_is_increasing = is_increasing_2
                    prev_val = val
                    continue

                # else we just remove the current one since the last one was legal
                continue
            if required_is_increasing != is_increasing and idx == 2 and len(arr) > 3: # possible to remove the first one here 
                # let's say we think the bad case is the first one, we change our "direction rule"
                # let's check if the next one is following this or even legal
                is_increasing_2, is_increasing_2 = is_legal_and_increasing(val, arr[idx+1])

                # next one is illegal anyways, so we're gone
                if not is_increasing_2:
                    is_all_legal = False
                    break
                # first one has to be removed, take this as the rule now
                if is_increasing == is_increasing_2:
                    required_is_increasing = is_increasing
                else:
                    # we remove this one and skip it
                    continue

            if not is_legal:
                continue
                
            prev_val = val
                
    if is_all_legal:
        legal += 1

print(legal)