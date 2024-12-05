

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
        
VALID_LETTERS = ['M', 'A']


def retrieve_item_safely(x, y, arr3d):
    if x < 0 or y < 0:
        return None
    try:
        return arr3d[x][y]
    except:
        return None 
    
# adjacent items
def scan_for_near_objects(x, y, letter, arr3d):
    correct_next_letters = []
    if letter in VALID_LETTERS:
        for [x_delta, y_delta] in DIAGONAL_COORDINATES:
            adjacent_item = retrieve_item_safely(x + x_delta, y+ y_delta, arr3d)  
            if adjacent_item == 'M' or adjacent_item == 'S':
                correct_next_letters.append({
                    "x": x + x_delta, 
                    "y": y+ y_delta, 
                    "letter": adjacent_item, 
                    })
        
    return correct_next_letters

DIAGONAL_COORDINATES = [[-1, 0], [-1, 1], [1, -1], [1,1]]
def is_diagonal_direction(x, y, next_letter):
    return [x - next_letter['x'], y-next_letter['y']] in DIAGONAL_COORDINATES


start_indexes = []
def solve_wordsearch(arr3d, mapping):
    for x, line in enumerate(arr3d):
        for y, letter in enumerate(line):
            if letter == 'A': # entry point
                start_indexes.append([x,y])
                mapping[x][y] = scan_for_near_objects(x, y, letter, arr3d)

    total_xs = 0
    for x, line in enumerate(mapping):
        for y, nearby_objects in enumerate(line):
            if len(nearby_objects) == 0 or arr3d[x][y] != 'A':
                continue 
            if  find_if_x([x,y], nearby_objects):
                total_xs+=1
    return total_xs
            
# {'x': 0, 'y': 1, 'letter': 'M'}, {'x': 0, 'y': 3, 'letter': 'S'}, {'x': 2, 'y': 1, 'letter': 'M'}, {'x': 2, 'y': 3, 'letter': 'S'}
DIAGONAL_COORDINATES = [[-1, -1],    [-1, 1], 
                        
                        
                        [1, -1],      [1,1]]

def get_opposite(coordinates):
    [x,y] = coordinates
    if [x,y] == [-1, -1]:
        return [1,1]
    elif [x,y] == [-1, 1]:
        return [1, -1]
    elif [x,y] == [1, -1]:
        return [-1, 1]
    elif [x,y] == [1, 1]:
        return [-1, -1]
    
    
def get_adjacent_sides(coordinates):
    [x,y] = coordinates
    if [x,y] == [-1, -1]:
        return [[-1,1], [1, -1]]
    elif [x,y] == [-1, 1]:
        return [[-1, -1], [1, 1]]
    elif [x,y] == [1, -1]:
        return [[-1,-1], [1, 1]]
    elif [x,y] == [1, 1]:
        return [[1,-1], [-1, 1]]

def base_unit_coordinate(a, coordinate):
    return [coordinate[0]- a[0], coordinate[1]-a[1]]
     

def find_if_x(a ,nearby_m_and_s):
    ms = [base_unit_coordinate(a, [mapping['x'], mapping['y']]) for mapping in nearby_m_and_s if mapping['letter'] == 'M'] 
    ss = [base_unit_coordinate(a, [mapping['x'], mapping['y']]) for mapping in nearby_m_and_s if mapping['letter'] == 'S'] 
    # print(ms)
    # print(ss)
    for m in ms:
        if get_opposite(m) in ss:
            adjacent_sides = get_adjacent_sides(get_opposite(m))
            for adjacent_side in adjacent_sides:
                if adjacent_side in ms and get_opposite(adjacent_side) in ss:
                    return True
                
    return False
    


arr3d, mapping = get_from_file()
print(solve_wordsearch(arr3d, mapping))