def get_from_file():
    f = open('input.txt', 'r')
    lines = []

    for line in f:
        arr = list(line)
        if arr[-1] == '\n':
            arr.pop()
        lines.append([int(val) for val in arr])

    # one line question
    return lines[0]


def get_value_from_index(index):
    return int(index / 2) if index % 2 == 0 else None  


# def get_fragemented_files(line_arr):
    

# 1 2 3, 3 is file, if len(file) % 2 == 0, 
# 1 2 3 4, 4 is space
def get_fragmented_files(line_arr):
    indexes_to_not_fill = {} # to not fill and the number it was
 
    # alternate between each number
    i = 0
    last_file_index = len(line_arr) - 1 if len(line_arr) % 2 == 1 else len(line_arr) -2 
    fragmented_files = []
    while i < len(line_arr):
        is_file = i % 2 == 0
        if last_file_index <= i and not is_file:
            fragmented_files += line_arr[i]*[0]
            i +=1
            continue
        if is_file:
            if i in indexes_to_not_fill.keys():
                fragmented_files += indexes_to_not_fill[i]*[0]
            else:
                fragmented_files += line_arr[i]*[get_value_from_index(i)]
            i += 1
        else: # we start adding from the back
            fragments_underfilled = line_arr[i] - line_arr[last_file_index]
            if fragments_underfilled < 0 or line_arr[last_file_index] <= 0: #  still some back files left
                # find next backfilled
                started_index = i
                last_index = last_file_index
                changed = False
                
                while last_index > started_index:
                    fragments_underfilled = line_arr[i] - line_arr[last_index]
                    
                    if fragments_underfilled < 0 or line_arr[last_index] <= 0:
                        last_index -=2
                    elif fragments_underfilled == 0:
                        fragmented_files += line_arr[i]*[get_value_from_index(last_index)]
                        indexes_to_not_fill[last_index] = line_arr[last_index]
                        line_arr[last_index] = 0
                        line_arr[i] = 0
                        i += 1
                        changed = True
                        break
                    elif fragments_underfilled > 0: # still some empty files left
                        fragmented_files += line_arr[last_index]*[get_value_from_index(last_index)]
                        indexes_to_not_fill[last_index] = line_arr[last_index]
                        line_arr[last_index] = 0
                        line_arr[i] = fragments_underfilled
                        changed = True
                        break
                if not changed:
                    # we just give up and i +=1
                    fragmented_files += line_arr[i]*[0]
                    i += 1
            elif fragments_underfilled == 0:
                fragmented_files += line_arr[i]*[get_value_from_index(last_file_index)]
                indexes_to_not_fill[last_file_index] = line_arr[last_file_index]
                line_arr[last_file_index] = 0
                line_arr[i] = 0
                last_file_index -= 2
                i += 1
            elif fragments_underfilled > 0: # still some space left, move on to the next back pointer
                fragmented_files += line_arr[last_file_index]*[get_value_from_index(last_file_index)]
                indexes_to_not_fill[last_file_index] = line_arr[last_file_index]
                line_arr[last_file_index] = 0
                line_arr[i] = fragments_underfilled
                last_file_index -= 2 # subtract 2 since -1 is an empty file space
           
        # breakpoint()
        
    return fragmented_files

def get_checksum(line_arr):
    result = get_fragmented_files(line_arr)
    return sum([i * val for i, val in enumerate(result)])

line_arr = get_from_file()
print(get_checksum(line_arr))