import copy
import numpy as np

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
    nearby_plants =[[nx, ny] for [nx, ny] in surroundings if  arr3d[ny][nx] == arr3d[y][x]]

    return [arr3d[y][x], nearby_plants]
    
    
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
 
 # adjacent coordinates
CORNER_TO_BLOCK_DELTAS = {tuple([0,0]) : [[0, -1], [-1,0]], tuple([1,0]): [[0, -1], [1, 0]], tuple([0,1]): [[-1, 0], [0, 1]], tuple([1,1]):[[0, 1], [1, 0]]}
CORNER_TO_ACROSS_DELTA = {tuple([0,0]) : [-1, -1], tuple([1,0]): [1, -1], tuple([0,1]): [-1, 1], tuple([1,1]):[1,1]}


def is_corner_check(arr3d, x, y, corner, corner_set):
  max_y = len(arr3d)-1
  max_x = len(arr3d[0])-1
  # if both adjacents are the same, there's a corner, if none are the same, there's also a corner (inverse)
  [a_dx, a_dy] = CORNER_TO_BLOCK_DELTAS[tuple(corner)][0]
  [b_dx, b_dy] = CORNER_TO_BLOCK_DELTAS[tuple(corner)][1]
  [c_dx, c_dy] = CORNER_TO_ACROSS_DELTA[tuple(corner)]
  letter_a = arr3d[a_dy+y][a_dx+x] if is_in_bound(x, y, a_dx, a_dy, max_x, max_y) else ' '
  letter_b = arr3d[b_dy+y][b_dx+x] if is_in_bound(x, y, b_dx, b_dy, max_x, max_y) else ' '
  letter_c = arr3d[c_dy+y][c_dx+x] if is_in_bound(x, y, c_dx, c_dy, max_x, max_y) else ' '
  letter = arr3d[y][x]
  
  # if everything is the same block, no corner
  if letter_a == letter and letter_b == letter and letter_c == letter:
     return False

  if letter == letter_c and letter_a != letter and letter_b != letter:
    # try adding existing corner, speciall case
    prev_corners_count = len(corner_set)
    corner_set.add(tuple([x+corner[0],y+corner[1]]))
    if len(corner_set) == prev_corners_count: #need to account for overlapping corner
      corner_set.add(tuple(["overlap: " + str(x+corner[0]),y+corner[1]]))
    return False
  # 
 
  return (letter_a == letter and letter_b == letter) or (letter_a != letter and letter_b != letter) or (letter_c == letter)
    

CORNER_DELTAS = [[0,0], [1,0], [0,1], [1,1]]
def get_corners(arr3d, x, y, corner_set):
  corners = corner_set.copy()
  for [c_dx, c_dy] in CORNER_DELTAS:
    is_corner = is_corner_check(arr3d, x, y, [c_dx, c_dy], corners)
    if is_corner:
      corners.add(tuple([x+c_dx,y+c_dy]))
  
  return corners

def collect_garden(nearby_plants, arr3d, garden_vals, corner_set):
  fence_area = 0
  for [x,y] in nearby_plants:
    [letter, new_nearby_plants] = garden_vals[y][x]
    if letter == '':
      continue

    corner_set |= get_corners(arr3d, x, y, corner_set)
    fence_area += 1
    garden_vals[y][x] = ['', []]
    
    if len(new_nearby_plants) > 0: 
      recursive_fence_area = collect_garden(new_nearby_plants, arr3d, garden_vals, corner_set)
      fence_area += recursive_fence_area

  return fence_area

def total_cost(arr3d, garden_vals):
  total = 0
  

  for y, line in enumerate(arr3d):
    for x, letter in enumerate(line):
      garden_vals[y][x] = get_fence_cost_letter(arr3d,x,y)
  
  for y, line in enumerate(garden_vals):
    for x, [letter, nearby_plants] in enumerate(line):
      if letter == '': # already counted
        continue
      else:
        test = [[' ' for y in range(0,len(garden_vals[0])+1)] for x in range(0,len(garden_vals)+1)]
        corner_set = (set() | get_corners(arr3d, x, y , set())).copy()
        garden_vals[y][x] = ['', []]
        total_fence_area = collect_garden(nearby_plants, arr3d, garden_vals, corner_set)
        total_fence_area += 1
        for corner in corner_set:
          try:
            test[corner[1]][corner[0]] = '.'
          except:
            pass
        cost = len(corner_set) * total_fence_area
        
        total += cost
        
  return total

print(total_cost(arr3d,mapping))

