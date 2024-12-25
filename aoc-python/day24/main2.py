import copy
from functools import reduce 

def split_input(line):
    [key, val] = line.strip().split(':')
    
    return key, int(val)

def split_output(line):
    [a, o, b, _, r] = line.replace('\n', '').split(' ')
    return [a,'AND',b,r]

def get_input_from_file():
    f = open('input.txt')
    inputs = {}
    outputs = []
    reading_inputs = True

    for line in f:
        if line == '\n' and reading_inputs:
            reading_inputs = False
            continue
        if line == '\n' and not reading_inputs:
            break

        if reading_inputs:
            key, val = split_input(line)
            inputs[key] = val
        else:
            outputs.append(split_output(line))

    return inputs, outputs


def calculate(val1, o, val2):
    if o == 'AND':
        return val1 & val2
    elif o == 'OR':
        return val1 | val2
    else:
        return val1 ^ val2

def add_obj(accumulator, item):
    accumulator[item[3]] = item
    return accumulator

# probably a bit less effiicent, but just going through all
# solving ones we can solve/skipping unsolved ones until done 
def solve_all_inputs(inputs, outputs):
    outputs_to_solve = reduce(add_obj, outputs, {})
    while len(outputs_to_solve) > 0:
        for key in list(outputs_to_solve.keys()):
            [a, o, b, r] = outputs_to_solve[key]
            if inputs.get(a, None) is None or inputs.get(b, None) is None:
                continue 
            r_val = calculate(inputs[a], o, inputs[b])
            inputs[r] = r_val 
            del outputs_to_solve[key]

    return inputs

def add(num1, num2):
    return int(bin(int(str(num1), 2) + int(str(num2), 2))[2:],2)

def get_output_expected(inputs):
    x_arr = []
    y_arr = []

    for key in inputs:
        if key[0] == 'x':
            x_arr.append(key)
        elif key[0] == 'y':
            y_arr.append(key)

    x_arr.sort()
    y_arr.sort()
    
    breakpoint()

def find_all_required_swaps(all_inputs, outputs: list):
    values = [r for [a,o,b,r] in outputs if r[0] == 'z']
    values.sort()
    i = len(values) -1
    answer = ""
    while i >= 0:
        answer += str(all_inputs[values[i]])
        
        i -= 1
    return int(answer, 2)

inputs, outputs = get_input_from_file()
all_inputs = solve_all_inputs(inputs,outputs)
output_expected = get_output_expected(inputs)
answer = find_all_required_swaps(all_inputs,outputs, output_expected)

print(answer)
        
            