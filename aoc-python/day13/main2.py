def read_line():
    f = open('input.txt', 'r')

    problems = []
    problem_set = {}
    TO_ADD = 10000000000000
    
    for line in f:
      if line == '\n':
        problems.append(problem_set)
        problem_set = {}
      elif 'Button A' in line:
        [_,x_add_str, y_add_str]  = line.split('+')
        x_add = int(x_add_str.split(',')[0])
        y_add = int(y_add_str)
        problem_set['A'] =[x_add, y_add]
      elif 'Button B' in line:
        [_,x_add_str, y_add_str]  = line.split('+')
        x_add = int(x_add_str.split(',')[0])
        y_add = int(y_add_str)
        problem_set['B'] =[x_add, y_add]
      else:
        [_,x_str, y_str]  = line.split('=')
        x = int(x_str.split(',')[0]) + TO_ADD
        y = int(y_str) + TO_ADD
        problem_set['Prize'] = [x,y]
  
    return problems

problems = read_line()

# print(problems)

def solve_for_a(problem):
  # RX - X_B*RY/Y_B = a*X_A - a *(Y_A*X_B/Y_B)
  
  right_side = problem['Prize'][0] - (problem['B'][0]*problem['Prize'][1]/problem['B'][1]) 
  left_side_a = problem['A'][0] - (problem['A'][1]*problem['B'][0]/problem['B'][1])
  
  a = right_side/left_side_a
  
  return a

def solve_for_b(problem, a):
  #  (R_X - (a*X_A))/X_B = b
  
  return (problem['Prize'][0] - a*problem['A'][0])/problem['B'][0]

def mathier_solve(problem):
  precision = 0.000000000000000001
  a_maybe_decimal = solve_for_a(problem)
  integer_part = int(a_maybe_decimal)
  decimal_difference = abs(a_maybe_decimal - integer_part)
  
  # if a_maybe_decimal != int(a_maybe_decimal) and ((not decimal_difference <= precision * integer_part)
  #                                             and decimal_difference <= precision_2 * integer_part) :
  #   # breakpoint()
  #   pass
  
  if decimal_difference <= precision * integer_part:
    print(a_maybe_decimal)
    a =a_maybe_decimal
  else:
    return None
  
  b_maybe_decimal = solve_for_b(problem, a)
  integer_part = int(b_maybe_decimal)
  decimal_difference = abs(b_maybe_decimal - integer_part)
  if decimal_difference <= precision * integer_part:
    print(b_maybe_decimal)
    b = b_maybe_decimal
  else:
    return None
    
  solve = lambda a, b: [a*(problem['A'][0]) + b*problem['B'][0], a*(problem['A'][1]) + b*problem['B'][1]]
  
  if solve(a_maybe_decimal,b_maybe_decimal) == problem['Prize']:
    return a*3 + b
  else:
    return None
  

def me_monkey_solve(problems):
  total = 0
  for problem in problems:
    
    lowest_solved = mathier_solve(problem)
    if lowest_solved is not None:
      total += lowest_solved
    
  print(total)
  
me_monkey_solve(problems)