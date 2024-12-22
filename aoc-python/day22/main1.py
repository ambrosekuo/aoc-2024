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

def get_sum_of_all_secret_numbers(secret_numbers, iterations= 2000):
    sum = 0
    for secret_number in secret_numbers:
        for i in range(iterations):
            secret_number = get_next_secret_number(secret_number)
        sum += secret_number
    
    return sum

print(get_sum_of_all_secret_numbers(secret_numbers))