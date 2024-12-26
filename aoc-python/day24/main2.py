import copy
from functools import reduce 

def split_input(line):
    [key, val] = line.strip().split(':')
    
    return key, int(val)

def split_output(line):
    [a, o, b, _, r] = line.replace('\n', '').split(' ')
    return [a,'ADD',b,r]

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
    if o == 'ADD':
    	return add(val1, val2)
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
    return bin(int(str(num1), 2) + int(str(num2), 2))[2:]
    
def minus(num1, num2):
    return bin(int(str(num1), 2) -  int(str(num2), 2))[2:]

def get_output_expected(inputs):
    x_arr = []
    y_arr = []

    for key in inputs:
        if key[0] == 'x':
            x_arr.append(key)
        elif key[0] == 'y':
            y_arr.append(key)

    x_arr.sort(reverse=True)
    y_arr.sort(reverse=True)
    x_bin = ''.join([str(inputs[key]) for key in x_arr])
    y_bin =  ''.join([str(inputs[key]) for key in y_arr])
    
    result = add(x_bin, y_bin)
    
    return str(result)

def bin_val(val, digit):
	trailing_0s = "0" * digit
	
	return str(val)+trailing_0s


def get_answer_arr(values, length):
    answer = 0
    i = 0
    while i < len(values):
        answer = add(bin_val(values[i], len(values)-i-1), answer)
        i += 1

    if len(answer) >= length:
        answer_arr = list(answer)
    elif len(answer) < length:
        answer_arr  = list(("0" * (length - len(answer))) + answer)
    
    return answer_arr

# Variants requiring changes/within 2 digits behind
# if im changing others, we kinda have to skip to it and add it as changes
VARIANTS = {
    "0": [
        ["0", None],
        ["1", "10"],
        ["10", None],
        #["1", "1", "10"], # maybe this is  cascading case and doesnt matter..
    ],
    "1": [
        ["1", None],
        ["0", "10"],
        ["10", "10"] # maybe we discard this case because we thought about it already...
    ],
    "10": [
        ["10", None],
        ["1", "10"]
    ],
    "11": [
        ["10", "11"],
    ],
}

def get_possible_changes(expected_arr, i):
    possible_changes = []
    # im pretty sure it can equal to each other and still require changes, maybe we look for cases anyways
    for [val, next_val] in VARIANTS[expected_arr[i]]:
        possible_changes.append([val, next_val])

    return possible_changes
        
        
    
# current
#  changes_made = [[index, new_val]]
def solve(expected_arr, z_values, i, changes_made, limit):
    if i >= len(expected_arr):
        return [changes_made]

    if len(changes_made) > limit:
        return []

    possible_changes = get_possible_changes(expected_arr, i)
    answer_arr = get_answer_arr(z_values, len(expected_arr))
    answers = []
    for [val, next_val] in possible_changes:
        if val == answer_arr[i] and val == expected_arr[i]:
            # if changes_made == [[0, '1'], [3, '0']]:
            #     breakpoint()
            sub_answers = solve(expected_arr, z_values, i+1, changes_made, limit)
            answers += sub_answers
            continue
        if next_val is None:
            sub_answers = solve(expected_arr, z_values, i+1, changes_made+[[i,val]], limit)
            answers += sub_answers
        else:
            # discard this
            if i+1 >= len(expected_arr):
                continue
            new_expected_arr = expected_arr.copy()
            new_expected_arr[i+1] = next_val
            sub_answers = solve(new_expected_arr, z_values, i+1, changes_made+[[i,val]], limit)
            answers += sub_answers
            
    return answers

# 100 
# 001 => lets say i need 0, i can either add 0 or 10. Or result of 1 10 => 100
# create mappings of each possibility and go down that path?
# lets say i do have it. i check through if it's possible to swap with others...
# cant retrieve from the bottom because the bottom combinations can affect the top/have to revisit
# can top affect bottom? no. if im too far that's fine, assume its same length for now
def find_all_swappable_choices(all_inputs, outputs: list, expected):
    z_mappings = [r for [a,o,b,r] in outputs if r[0] == 'z']
    z_mappings.sort(reverse=True)
    i = 0 #len(values) -1
    answer = 0
    while i < len(z_mappings):
        answer = add(bin_val(all_inputs[z_mappings[i]], i), answer)
        
        i += 1
    if len(answer) > len(expected):
        expected_arr  = list(("0" * (len(answer) - len(expected))) + expected)
    elif len(answer) <= len(expected):
        expected_arr = list(expected)

    z_values = [all_inputs[z_name] for z_name in z_mappings]
        
    answers = solve(expected_arr, z_values, 0, [], 8) # at least we can hardcode this lmao

    return answers, len(z_mappings)

def get_inputs_inverse(inputs):
    return {key: [name for name in inputs if inputs[name] == key] for key in set(inputs.values())} 

# we're counting backwards, with max z at front
# i = 4
def get_z_name_from_index(i, z_count):
    return "z{:03}".format(z_count-i)

def get_swaps(changes_needed, swapped, z_length):
    for [z_i, val] in changes_needed:
        get_z_name_from_index(z_i, z_length)
    

def get_swap_solutions(answers, all_inputs, z_length):
    val_to_name = get_inputs_inverse(all_inputs)
    breakpoint()
    for changes_needed in answers:
        sol = get_swaps(changes_needed, {}, z_length)
        if sol:
            return sol
    

inputs, outputs = get_input_from_file()

all_inputs = solve_all_inputs(inputs,outputs)
output_expected = get_output_expected(inputs)
answers, z_length = find_all_swappable_choices(all_inputs, outputs, output_expected)
swap_names = get_swap_solutions(answers, all_inputs, z_length)

# print(answer)
        
            