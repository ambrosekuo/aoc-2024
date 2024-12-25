import heapq

def read_from_file():
    with open("input.txt") as f:
        grid = []
        start = None
        end = None

        for y, line in enumerate(f):
            arr = list(line.strip())
            if 'S' in arr:
                start = [arr.index('S'), y]
            if 'E' in arr:
                end = [arr.index('E'), y]
            grid.append(arr)

        return grid, start, end

def key(coordinate):
    x, y = coordinate
    return f"{x},{y}"

POSSIBLE_PATHS_DELTAS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

def get_reachable_paths(grid, current):
    x, y = current
    reachable_paths = []
    for dx, dy in POSSIBLE_PATHS_DELTAS:
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] in {'.', 'E'}:
                reachable_paths.append([nx, ny])
    return reachable_paths

def calculate_next_direction_and_points(current, direction, next_path):
    x, y = current
    nx, ny = next_path
    new_direction = [nx - x, ny - y]
    if direction != new_direction:
        return new_direction, 1001  # Higher cost for changing direction
    else:
        return new_direction, 1  # Lower cost for continuing in the same direction

def get_lowest_points(grid, start, end):
    priority_queue = []
    visited = set()
    weighted_map = {key(start): 0}
    initial_direction = [1, 0]

    heapq.heappush(priority_queue, (0, start, initial_direction))  # (points, position, direction)

    while priority_queue:
        current_points, current, direction = heapq.heappop(priority_queue)
        if key(current) in visited:
            continue

        visited.add(key(current))

        if current == end:
            return current_points

        for next_path in get_reachable_paths(grid, current):
            next_direction, step_cost = calculate_next_direction_and_points(current, direction, next_path)
            total_points = current_points + step_cost

            if total_points < weighted_map.get(key(next_path), float('inf')):
                weighted_map[key(next_path)] = total_points
                heapq.heappush(priority_queue, (total_points, next_path, next_direction))

    return float('inf')  # Return infinity if the path to 'E' is unreachable

# Read input and compute the lowest points
grid, start, end = read_from_file()
print(get_lowest_points(grid, start, end))
