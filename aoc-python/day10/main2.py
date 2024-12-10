def get_from_file():
    f = open('input.txt', 'r')

    arr3d = []
    mapping = []

    for line in f:
        arr = list(line)
        if arr[-1] == '\n':
            arr.pop()
        arr3d.append([int(val) if val != '.' else val for val in arr ])
        mapping.append([{} for x in arr])

    return arr3d, mapping

arr3d, mapping = get_from_file()

NEXT_PATHS_DELTA = [[0,-1], [1, 0], [-1,0], [0, 1]]
def get_next_possible_paths(arr3d, x, y):
    bounding_y = len(arr3d)
    bounding_x = len(arr3d[0])
    next_paths = []
    for [delta_x, delta_y] in NEXT_PATHS_DELTA:
        [next_x, next_y] = [delta_x+x, delta_y + y]
        if next_x < bounding_x and next_y < bounding_y and next_x >= 0 and next_y >= 0:
            if arr3d[next_y][next_x] == arr3d[y][x] +1:
                next_paths.append([next_x, next_y])
                
    return next_paths


def get_trailhead_ends(arr3d, x, y):
    if arr3d[y][x] == 9:
        return 1
    
    trails = 0
    for [next_x, next_y] in get_next_possible_paths(arr3d, x,y):
        trails += get_trailhead_ends(arr3d, next_x, next_y)
    
    return trails
    
def get_trails(arr3d):
    total_trailhead_scores = 0
    for y, line in enumerate(arr3d):
        for x, val in enumerate(line):
            if val == 0:
                total_trailhead_scores += get_trailhead_ends(arr3d, x, y)

    return total_trailhead_scores

print(get_trails(arr3d))