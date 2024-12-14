def read_line():
    f = open('input.txt', 'r')

    problems = []
    problem_set = {}
    
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
        x = int(x_str.split(',')[0])
        y = int(y_str)
        problem_set['Prize'] = [x,y]
  
    return problems

problems = read_line()

def fancy_solve(problem):
  a = 0
  lowest_solved = None
  solve = lambda a, b: [a*(problem['A'][0]) + b*problem['B'][0], a*(problem['A'][1]) + b*problem['B'][1]]
  
  while a <= 100:
    b = 0
    while b <= 100:
      if solve(a,b) == problem['Prize'] and (lowest_solved is None or lowest_solved > (3*a+b)):
        lowest_solved = (3*a)+b
      b += 1
    a += 1
    
  return lowest_solved

def me_monkey_solve(problems):
  total = 0
  for problem in problems:
    lowest_solved = fancy_solve(problem)
    if lowest_solved is not None:
      total += lowest_solved
    
  print(total)
  
me_monkey_solve(problems)