

def get_from_file():
    f = open('input.txt', 'r')

    arr3d = []
    mapping = []

    for line in f:
        arr = list(line)
        if arr[-1] == '\n':
            arr.pop()
        arr3d.append(arr)
        mapping.append([{} for x in arr])

    return arr3d, mapping
        
next_letter_mapping = {
    'X': 'M',
    'M': 'A',
    'A': 'S',
    'S': None
}
VALID_LETTERS = ['X', 'M', 'A']

def is_next_letter(letter1, letter2):
    return next_letter_mapping[letter1] == letter2

def retrieve_item_safely(x, y, arr3d):
    if x < 0 or y < 0:
        return None
    try:
        return arr3d[x][y]
    except:
        return None 
    
# adjacent items
combinations = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1,1]]
def scan_for_near_objects(x, y, letter, arr3d):
    correct_next_letters = []
    if letter in VALID_LETTERS:
        for [x_delta, y_delta] in combinations:
            adjacent_item = retrieve_item_safely(x + x_delta, y+ y_delta, arr3d)  
            # print([x + x_delta, y+ y_delta, letter, adjacent_item])
            if is_next_letter(letter, adjacent_item):
                correct_next_letters.append({
                    "x": x + x_delta, 
                    "y": y+ y_delta, 
                    "letter": adjacent_item, 
                    })
        
    return correct_next_letters

def traverse_count(x, y, letter, arr3d, mapping, direction_limit):
    if letter == 'S': # we made a full traversal
        return 1
    next_letters = mapping[x][y]
    total_traversal_count = 0
    for next_letter in next_letters:
        new_direction_limit = direction_limit
        if new_direction_limit is not None:
            # skip if not expected direction
            if next_letter['x']-x != direction_limit[0] or next_letter['y']-y != direction_limit[1]:
                continue
        else:
            new_direction_limit = [next_letter['x']-x, next_letter['y']-y]
        total_traversal_count += traverse_count(next_letter['x'], next_letter['y'], next_letter['letter'], arr3d, mapping, new_direction_limit)

    return total_traversal_count
        

start_indexes = []
def solve_wordsearch(arr3d, mapping):
    for x, line in enumerate(arr3d):
        for y, letter in enumerate(line):
            if letter == 'X': # entry point
                start_indexes.append([x,y])
            mapping[x][y] = scan_for_near_objects(x, y, letter, arr3d)
            
    total_words_found = 0
    for [x,y] in start_indexes:
        direction_limit = None
        total_words_found += traverse_count(x, y, 'X', arr3d, mapping, direction_limit)
        
    return total_words_found

arr3d, mapping = get_from_file()
print(solve_wordsearch(arr3d, mapping))