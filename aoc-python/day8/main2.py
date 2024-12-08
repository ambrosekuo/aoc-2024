
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

# [5, 2], [7, 3]
# expected: 
# [3, 1], [7, 4]
# [2, 1], [3, 1], [9, 4]

def out_of_bounds(arr3d, coordinate):
    [x, y] = coordinate
    bounding_y = len(arr3d)-1
    bounding_x = len(arr3d[0])-1
    if x < 0 or y < 0:
        return True
    elif x > bounding_x or y > bounding_y:
        return True 
    
    return False

def travel_anti_node_path(antinodes, node, increment, non_antinodes):
    new_node = [node[0] + increment[0], node[1] + increment[1]]
    if not out_of_bounds(arr3d, node) and tuple(new_node) not in non_antinodes:
        antinodes.add(tuple(node))
        travel_anti_node_path(antinodes, new_node, increment, non_antinodes)
    else: 
        return 
    
# [4, 4] , [8, 1]
# [4, -3], 
def get_antinodes(arr3d, coordinate1, coordinate2):
    [diff_x, diff_y] = [coordinate1[0]-coordinate2[0], coordinate1[1]-coordinate2[1]]
    antinodes = set()
    non_antinodes = set()

    if diff_x % 2 == 0 and diff_y % 2 == 0:
        non_antinodes.add([coordinate1[0]-diff_x/2, coordinate1[1]-diff_y/2])

    for [x,y] in [coordinate1, coordinate2]:
        travel_anti_node_path(antinodes, [x,y], [diff_x, diff_y], non_antinodes)
        travel_anti_node_path(antinodes, [x,y], [-diff_x, -diff_y], non_antinodes)

    return antinodes

def get_all_antinodes(arr3d, coordinates_for_letter):
    antinodes = set()
    for i, coordinate_1 in enumerate(coordinates_for_letter):
        if i+1 == len(coordinates_for_letter):
            break
        for j, coordinate_2 in enumerate(coordinates_for_letter[i+1:]):
            print((coordinate_1,coordinate_2), get_antinodes(arr3d, coordinate_1, coordinate_2))
            antinodes |= (get_antinodes(arr3d, coordinate_1, coordinate_2))
    
    print(print(antinodes))
    return antinodes

def get_antinodes_count(arr3d):
    letters_to_coordinates = {}
    answers = set()
    for y, line in enumerate(arr3d):
        for x, val in enumerate(line):
            if val == '.':
                continue
            if val == '#':
                answers.add(tuple([x,y]))
                continue
            coordinates_for_letter = letters_to_coordinates.get(val, None)
            if coordinates_for_letter is None:
                letters_to_coordinates[val] = [[x,y]]
            else:
                letters_to_coordinates[val].append([x,y])
    
    all_antinodes = set()
    for [letter, coordinates] in letters_to_coordinates.items():
        print(letter)
        all_antinodes |= (get_all_antinodes(arr3d, coordinates))
    # print('difference')
    # print(answers.difference(all_antinodes))

    return len(all_antinodes)

    
# loop through all the letters
arr3d, mapping = get_from_file()
print(get_antinodes_count(arr3d))