import copy

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
    
    # i think connected doesnt matter

NEXT_PATHS_DELTA = [[0,-1], [1, 0], [-1,0], [0, 1]]

def is_in_bound(x, y, delta_x, delta_y, max_x, max_y):
	x_in_bound = x+ delta_x >= 0 and x+delta_x <= max_x
	y_in_bound = y+ delta_y >= 0 and y+delta_y <= max_y
	return x_in_bound and y_in_bound
	
	
def get_fence_cost(arr3d, x, y):
    surroundings = [[delta[0]+x, delta[1]+y] for delta in NEXT_PATHS_DELTA if is_in_bound(x, y, delta[0], delta[1], len(arr3d[0])-1, len(arr3d)-1)]
    fence_count = sum([1 for [nx, ny] in surroundings if  arr3d[ny][nx] != arr3d[y][x]]) + (4- len(surroundings))
    
    same_plants =[[nx, ny] for [nx, ny] in surroundings if  arr3d[ny][nx] == arr3d[y][x]]
    return same_plants, fence_count

	
def get_fence_cost_letter(arr3d, x, y):
    surroundings = [[delta[0]+x, delta[1]+y] for delta in NEXT_PATHS_DELTA if is_in_bound(x, y, delta[0], delta[1], len(arr3d[0])-1, len(arr3d)-1)]
    fence_count = sum([1 for [nx, ny] in surroundings if  arr3d[ny][nx] != arr3d[y][x]]) + (4- len(surroundings))
    nearby_plants =[[nx, ny] for [nx, ny] in surroundings if  arr3d[ny][nx] == arr3d[y][x]]

    return [arr3d[y][x], fence_count, nearby_plants]
    
    
arr3d, mapping = get_from_file()

# openings'

def key(x,y):
	return f"{x},{y}"
	
	# merge into old build
def combine_gardens(old_build_key, new_build_key, fence_build, fence_openings):
	old_build = fence_build[old_build_key]
	new_build = fence_build[new_build_key]

	old_build["fence_sum"] += new_build["fence_sum"]
	old_build["fence_area"] += new_build["fence_area"]

	for fence_key in new_build["fence_openings"].keys():
		fence_openings[fence_key] = old_build_key
		old_build["fence_openings"][fence_key] = True
	
	del new_build

def collect_garden(nearby_plants, garden_vals):
	fence_count = 0
	fence_area = 0
	for [x,y] in nearby_plants:
		[letter, path_fence_count, new_nearby_plants] = garden_vals[y][x]
		if letter == '':
			continue

		fence_count += path_fence_count
		fence_area += 1
		garden_vals[y][x] = ['', 0, []]
		
		if len(new_nearby_plants) > 0: 
			recursive_fence_area, recursive_fence_count = collect_garden(new_nearby_plants, garden_vals)
			fence_area += recursive_fence_area
			fence_count += recursive_fence_count

	return fence_area, fence_count

def total_cost(arr3d, garden_vals):
	total = 0

	for y, line in enumerate(arr3d):
		for x, letter in enumerate(line):
			garden_vals[y][x] = get_fence_cost_letter(arr3d,x,y)
	
	for y, line in enumerate(garden_vals):
		for x, [letter, fence_count, nearby_plants] in enumerate(line):
			if letter == '': # already counted
				continue
			else:
				garden_vals[y][x] = ['', 0, []]
				total_fence_area, total_fence_count = collect_garden(nearby_plants, garden_vals)
				total_fence_area += 1
				total_fence_count += fence_count
				cost = total_fence_count * total_fence_area
				total += cost
				
	return total

print(total_cost(arr3d,mapping))
