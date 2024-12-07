
def get_from_file():
    f = open('input.txt', 'r')
    
    equations = []
    
    for line in f:
        answer = int(line.split(":")[0])
        values = [int(value) for value in line.split()[1:]]
        equations.append([answer, values])

    return equations

def can_equation_combinations_be_solved(equation):
    [answer, values] = equation
    values_variation = values.copy()
    results = []
    for i, val in enumerate(equation[:-1]):
        numb1 = values_variation[i]
        numb2 = values_variation[i+1]
        del values_variation[i+1]

        values_deviation_1 = numb1 * numb2
        values_deviation_2 = numb1 + numb2
        values_variation[i] = values_deviation_1
        results.append(can_equation_be_solved([answer, values_variation]))
        values_variation[i] = values_deviation_2
        results.append(can_equation_be_solved([answer, values_variation]))

    return any(results)
        
# 14 5 1 2 case wheere, you need to vary it
# equation = [answer, [val1, val2,...]]
def can_equation_be_solved(equation):
    [answer, values] = equation
    if len(values) == 1 and answer == values[0]:
        return True
    if len(values) == 1 and answer != values[0]:
        return False
    else:
        return can_equation_combinations_be_solved(equation)


def get_correct_sum(equations):
    sum = 0
    for [answer, values] in equations:
        if can_equation_be_solved([answer, values]):
           sum += answer
    
    return sum
            

equations = get_from_file()
print(get_correct_sum(equations))