

def get_from_file():
    f = open('sample_input.txt', 'r')

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
    'M': 'A',
    'A': 'S',
    'S': None
}
VALID_LETTERS = ['M', 'A']

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

DIAGONAL_COORDINATES = [[-1, 0], [-1, 1], [1, -1], [1,1]]
def is_diagonal_direction(x, y, next_letter):
    return [x - next_letter['x'], y-next_letter['y']] in DIAGONAL_COORDINATES


def traverse_array(x, y, letter, arr3d, mapping, direction_limit):
    if letter == 'S': # we made a full traversal
        return [[x,y]]
    next_letters = mapping[x][y]
    diagonals = []
    for next_letter in next_letters:
        new_direction_limit = direction_limit
        if new_direction_limit is not None:
            # skip if not expected direction
            if next_letter['x']-x != direction_limit[0] or next_letter['y']-y != direction_limit[1]:
                continue
        else:
            if is_diagonal_direction(x,y, next_letter):
                new_direction_limit = [next_letter['x']-x, next_letter['y']-y]
            else:
                continue
        
        current_letter = [x,y]
        rest_of_chain = traverse_array(next_letter['x'], next_letter['y'], next_letter['letter'], arr3d, mapping, new_direction_limit)

        diagonals.append(current_letter)
        diagonals = diagonals + rest_of_chain
    return diagonals
        

start_indexes = []
def solve_wordsearch(arr3d, mapping):
    for x, line in enumerate(arr3d):
        for y, letter in enumerate(line):
            if letter == 'M': # entry point
                start_indexes.append([x,y])
            mapping[x][y] = scan_for_near_objects(x, y, letter, arr3d)
            
    diagonal_coordinates = []
    for [x,y] in start_indexes:
        direction_limit = None
        diagonals_mas = traverse_array(x, y, 'M', arr3d, mapping, direction_limit)
        if len(diagonals_mas) > 0:
            diagonal_coordinates.append(diagonals_mas)
        
    # print(diagonal_coordinates)
    # overlaps
    tracked_overlaps = {}
    for diagonal_sets in diagonal_coordinates:
        start = diagonal_sets[0].copy()
        del diagonal_sets[0]
        count = 1

        for idx, item in enumerate(diagonal_sets):
            if diagonal_sets[idx] == start:
                count = 1
                
            count +=1
            if count == 3:
                unique_coordinate_of_m = str(diagonal_sets[idx-1][0])+"," + str(diagonal_sets[idx-1][1])
                if tracked_overlaps.get(unique_coordinate_of_m, None) is None:
                    tracked_overlaps[unique_coordinate_of_m] = 0
                else:
                    tracked_overlaps[unique_coordinate_of_m] +=1


    print(len(tracked_overlaps.keys()))
    return sum(tracked_overlaps.values())

arr3d, mapping = get_from_file()
print(solve_wordsearch(arr3d, mapping))