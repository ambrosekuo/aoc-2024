import math
from datetime import datetime

def get_from_file():
    f = open('input.txt', 'r')

    numbers = [int(val) for val in f.read().split()]

    return numbers

numbers = get_from_file()

def get_digits(number):
    return len(str(number))

def apply_rules(number):
    if number == 0:
        return [1]
    if get_digits(number) % 2 == 0:
        str_number = str(number)
        split_1 = int(str_number[:int(len(str_number)/2)])
        split_2 = int(str_number[int(len(str_number)/2):])
        return [split_1, split_2]
    
    return [number * 2024]


def get_stone_count(numbers, current_blinks, blinks_target):
    if current_blinks == blinks_target:
        return len(numbers)
    
    count = 0
    for i, number in enumerate(numbers):
        number_list = apply_rules(number) 
        numbers[i] = number_list[0] # guaranteed first number
        if len(number_list) == 2:
            count += get_stone_count([number_list[1]], current_blinks+1, blinks_target)

    return get_stone_count(numbers, current_blinks+1, blinks_target) + count


def get_stones(numbers, blinks):
    return get_stone_count(numbers, 0, blinks)


start_time = datetime.now()
stones_count = get_stones(numbers, 30)
print(stones_count)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))