def get_from_file():
    game_area = []
    f = open('input.txt')
    
    for line in f:
        arr = list(line)
        if arr[-1] == '\n':
            del arr[-1]

        game_area.append(arr)

    return game_area

def find_game_start(game_area):
    for y, line in enumerate(game_area):
        for x, letter in enumerate(line):
            if letter == 'S':
                return [x,y]

POSSIBLE_PATHS_DELTAS = [[0,-1], [1,0], [0,1], [-1, 0]]
def get_next_path(game_area, current, path_travelled):
    [x,y] = current
    for [dx, dy] in POSSIBLE_PATHS_DELTAS:
        try:
            if [dx+x,dy+y] in path_travelled:
                continue
            if game_area[dy+y][dx+x] == '.':
                return [dx+x, dy+y], False
            if game_area[dy+y][dx+x] == 'E':
                return [dx+x,dy+y], True
        except:
            continue
    # shouldn't be able to return a dead end..
            
def key(coordinate):
    [x,y] = coordinate
    return f"{x},{y}"

def get_traversal(game_area, start):
    current = start
    path = [start] # keeps an order
    path_map = {key(start): 0}
    while True:
        next_path, is_end = get_next_path(game_area, current, path)
        current = next_path
        path.append(next_path)
        path_map[key(current)] = len(path) - 1
        if is_end:
            break
    return path, path_map

def get_cheat_coordinates(game_area, current):
    [x,y] = current
    all_cheat_ends = []
    for [dx, dy] in POSSIBLE_PATHS_DELTAS:
        try:
            if game_area[dy+y][dx+x] == '#':
                [cx,cy] = [dx+x, dy+y]
                for [d2x, d2y] in POSSIBLE_PATHS_DELTAS:
                    try:
                        if game_area[cy+d2y][cx+d2x] == '.' or game_area[cy+d2y][cx+d2x] == 'E':
                            all_cheat_ends.append([cx+d2x, cy+d2y])
                    except:
                        continue
        except:
            continue

    return all_cheat_ends
    
def get_cheats_count(game_area, path, path_map,  min_cheats = 100):
    cheat_count = 0
    cheats = []
    for [x, y] in path:
        cheat_endings = get_cheat_coordinates(game_area, [x,y])
        for [cx, cy] in cheat_endings:
            if path_map[key([cx,cy])] - path_map[key([x,y])]-2 >= min_cheats:
                cheats.append([[x,y], [cx,cy]])
                cheat_count+=1

    return cheat_count

map = get_from_file()
start = find_game_start(map)
path, path_map = get_traversal(map, start)
print(get_cheats_count(map, path, path_map))