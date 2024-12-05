
def get_from_file():
    f = open('input.txt', 'r')
    
    page_rules = []
    page_expected_updates = []

    is_recording_page_rules = True
    
    for line in f:
        if is_recording_page_rules:
            pages = line.rstrip().split("|")
            if len(pages) == 2:
                page_rules.append(pages)
            else:
                is_recording_page_rules = False
                continue
        else:
            page_expected_updates.append(line.rstrip().split(','))
            
    return page_rules, page_expected_updates


def is_page_expected_update_correct(page_rules, page_expected_update):
    for [lower_number, higher_number] in page_rules:
        try:
            if (page_expected_update.index(lower_number) > page_expected_update.index(higher_number)):
                return False
        except:
            continue
        
    return True
            

def get_sum_of_fixed_incorrect_middle_numbers(page_rules, page_expected_updates):
    # page_order = get_page_order(page_rules)
    sum = 0
    for page_expected_update in page_expected_updates:
        if not is_page_expected_update_correct(page_rules, page_expected_update):
            fixed_page_updates = spam_fix_incorrect_updates(page_rules, page_expected_update)
            sum += int(fixed_page_updates[int((len(fixed_page_updates)-1)/2)])

    return sum

def fix_incorrect_updates(page_rules, page_expected_update):
    page_corrected_update = page_expected_update.copy()
    for [lower_number, higher_number] in page_rules:
        try:
            if (page_corrected_update.index(lower_number) > page_corrected_update.index(higher_number)):
                former_low_index = page_corrected_update.index(lower_number)
                former_high_index = page_corrected_update.index(higher_number)
                page_corrected_update[former_low_index] = higher_number
                page_corrected_update[former_high_index] = lower_number
                
        except:
            continue
    return page_corrected_update

def spam_fix_incorrect_updates(page_rules, page_expected_update, count=5):
    counter = 0 
    fixed_page_expected_update = page_expected_update.copy()
    while counter < count:
        fixed_page_expected_update = fix_incorrect_updates(page_rules, fixed_page_expected_update)
        counter +=1
    return fixed_page_expected_update


# page_rules , index 0 always before 1, [x,y], 
page_rules, page_expected_updates = get_from_file()

sum = get_sum_of_fixed_incorrect_middle_numbers(page_rules, page_expected_updates)
