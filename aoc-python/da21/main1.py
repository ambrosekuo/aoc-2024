
for line in f:
    [el1, el2] = line.split()
    arr1.append(el1)
    arr2.append(el2)
    
    
GRID_CONTROL = [['X', '^', 'A'], ['<', 'v', '>']]

def get_letter_mapping(grid):
  letter_mapping = {}
  for y, arr in enumerate(grid):
     for x, item in enumerate(arr):
          letter_mapping[item] = [x, y]
  return letter_mapping

GRID_MAPPING = get_letter_mapping(GRID_CONTROL)
def get_travel_path(box1, box2):
    path = []
    
   