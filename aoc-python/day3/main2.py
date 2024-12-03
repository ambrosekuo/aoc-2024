
f = open('input.txt', 'r')

content = f.read()

print(content)


# rules:
# has to start with mul(
# has to have <number>,<number>)

total = 0


INIT_CONDITIONS = ['m', 'u', 'l', '(']
CONDITIONS_REQUIREMENT = ['m', 'u', 'l', '(', 'num1', 'comma', 'num2', 'closing']
conditions_arr = CONDITIONS_REQUIREMENT.copy()
VALID_NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
num1 = ''
num2 = ''

DO_CONDITION = ['d', 'o', '(', ')']
DONT_CONDITION = ['d', 'o', 'n', '\'', 't', '(', ')']
negation_condition = DONT_CONDITION.copy()
is_mul_enabled = True


for str in content:
    if len(negation_condition) == 0:
        is_mul_enabled = not is_mul_enabled
        if is_mul_enabled:
            negation_condition = DONT_CONDITION.copy()
        else: 
            negation_condition = DO_CONDITION.copy()

    if negation_condition[0] == str:
        del negation_condition[0]
        continue
    else:
        if is_mul_enabled:
            negation_condition = DONT_CONDITION.copy()
        else: 
            negation_condition = DO_CONDITION.copy()

    if not is_mul_enabled:
        continue

    if conditions_arr[0] in INIT_CONDITIONS:
        if conditions_arr[0] != str:
            conditions_arr = CONDITIONS_REQUIREMENT.copy()
            continue
        else:
            del conditions_arr[0]
            continue
    if conditions_arr[0] == 'num1' and str in VALID_NUMBERS:
        num1 += str
        continue
    if conditions_arr[0] == 'num1' and len(num1) > 0 and str == ',':
        del conditions_arr[0] #num1
        del conditions_arr[0] #comma
        continue

    if conditions_arr[0] == 'num2' and str in VALID_NUMBERS:
        num2 += str
        continue
    if conditions_arr[0] == 'num2' and len(num2) > 0 and str == ')':
        # reset all
        total += int(num1) * int(num2)
        conditions_arr = CONDITIONS_REQUIREMENT.copy()
        num1 = ''
        num2 = ''
        continue
    
    # if reached here, not valid 
    conditions_arr = CONDITIONS_REQUIREMENT.copy()
    num1 = ''
    num2 = ''

print(total)
    