import math 


def get_from_file():
    f = open('input.txt', 'r')
    secret_numbers = []

    for line in f:
        secret_numbers.append(int(line.split()[0]))

    return secret_numbers
    
    # i think connected doesnt matter

secret_numbers = get_from_file()

def mix(result, secret_number):
    return result^secret_number

def prune(secret_number):
    MODULO_CONST = 16777216
    return secret_number % MODULO_CONST

def get_next_secret_number(secret_number):
    # step1
    result = secret_number * 64
    secret_number = prune(mix(result, secret_number))
    # step 2
    result = math.floor(secret_number/32)
    secret_number = prune(mix(result, secret_number))
    # step 3
    result = secret_number * 2048
    secret_number = prune(mix(result, secret_number))

    return secret_number

def get_secret_numbers_iterations(secret_numbers, iterations= 2000):
    secret_numbers_iterations = []
    for secret_number in secret_numbers:
        secret_number_iterations = [secret_number]
        for i in range(iterations):
            secret_number = get_next_secret_number(secret_number)
            secret_number_iterations.append(secret_number)
        secret_numbers_iterations.append(secret_number_iterations)
    
    return secret_numbers_iterations

# arr of 4
def key(differences):
    [a,b,c,d]= differences
    return f"{a},{b},{c},{d}"

# idk how to name this man
def get_sequences_mappings(secret_numbers_iterations):
    all_sequences_encounters = set()
    secret_numbers_to_sequences_bananas_mapping = []
    for secret_number_iterations in secret_numbers_iterations:
        sequence_to_highest_bananas= {}
        for i, secret_number in enumerate(secret_number_iterations):
            if i >= 4:
                j = 3
                difference_arr = []
                while (j >= 0):
                    current_bananas = int(str(secret_number_iterations[i-j])[-1]) 
                    prev_bananas = int(str(secret_number_iterations[i-j-1])[-1])
                    difference = current_bananas-prev_bananas
                    difference_arr.append(difference)
                    j -= 1
                bananas = int(str(secret_number)[-1])
                diffs_key = key(difference_arr)
                if sequence_to_highest_bananas.get(diffs_key) is None:
                    sequence_to_highest_bananas[diffs_key] = bananas
                
                all_sequences_encounters.add(key(difference_arr))
        secret_numbers_to_sequences_bananas_mapping.append(sequence_to_highest_bananas)
    
    return secret_numbers_to_sequences_bananas_mapping, all_sequences_encounters

def get_highest_banana_sum(secret_numbers_to_sequences_bananas_mapping, all_sequences_encounters):
    highest_banana_sequence = 0
    for sequence_key in all_sequences_encounters:
        total_banana_count_for_sequence = 0 
        for secret_number_max_banana_mapping in secret_numbers_to_sequences_bananas_mapping:
            if secret_number_max_banana_mapping.get(sequence_key):
                total_banana_count_for_sequence += secret_number_max_banana_mapping[sequence_key]
        if total_banana_count_for_sequence > highest_banana_sequence:
            highest_banana_sequence = total_banana_count_for_sequence

    return highest_banana_sequence

secret_numbers_iterations = get_secret_numbers_iterations(secret_numbers)
secret_numbers_to_sequences_bananas_mapping, all_sequences_encounters = get_sequences_mappings(secret_numbers_iterations)
print(get_highest_banana_sum(secret_numbers_to_sequences_bananas_mapping,all_sequences_encounters))
