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

def add_or_create_pile(stone_piles, key, stones_to_add):
    if stone_piles.get(key, None) is None:
            stone_piles[key] = stones_to_add
    else:
        stone_piles[key] += stones_to_add


def stone_piles_after_blinks(numbers, current_blinks, blinks_target):
    stone_piles = {} 
    for number in numbers:
        add_or_create_pile(stone_piles, number, 1)

    # Important thing here is to have 2 separate stone piles, when you're splitting a stone
    # into two, you don't want to throw it in the old pile that you're moving. So we're in a state
    # where we're in between two piles. 
    while current_blinks < blinks_target:
        new_stone_piles = {}
        for key in stone_piles.keys():
            stones_count = stone_piles[key]
            stones_numbers = apply_rules(key)
            add_or_create_pile(new_stone_piles, stones_numbers[0], stones_count)
            if len(stones_numbers) == 2:
                add_or_create_pile(new_stone_piles, stones_numbers[1], stones_count)
                
        stone_piles = new_stone_piles
        current_blinks += 1


    return stone_piles


def get_stones(numbers, blinks):
    return sum([count for count in stone_piles_after_blinks(numbers, 0, blinks).values()])

start_time = datetime.now()
print(get_stones(numbers, 75))
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
