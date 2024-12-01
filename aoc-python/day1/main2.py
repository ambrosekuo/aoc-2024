f = open('input.txt', 'r')

arr1 = []
arr2 = []

for line in f:
    [el1, el2] = line.split()
    arr1.append(int(el1))
    arr2.append(int(el2))

arr1.sort()
arr2.sort()

arr1_obj = {}

for el in arr1:
    arr1_obj[el] = 0

for el in arr2:
    val = arr1_obj.get(el)
    if val is not None:
        arr1_obj[el] +=1

sum = 0        
for key in arr1_obj.keys():
    sum += arr1_obj[key] * key

print(sum)