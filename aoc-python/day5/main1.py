
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
            

def get_sum_of_correct_middle_numbers(page_rules, page_expected_updates):
    # page_order = get_page_order(page_rules)
    sum = 0
    for page_expected_update in page_expected_updates:
        if is_page_expected_update_correct(page_rules, page_expected_update):
            sum += int(page_expected_update[int((len(page_expected_update)-1)/2)])

    return sum
        

# page_rules , index 0 always before 1, [x,y], 
page_rules, page_expected_updates = get_from_file()

sum = get_sum_of_correct_middle_numbers(page_rules, page_expected_updates)
print(sum)
