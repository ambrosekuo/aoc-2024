f = open('input.txt', 'r')

arr1 = []
arr2 = []

for line in f:
    [el1, el2] = line.split()
    arr1.append(el1)
    arr2.append(el2)

arr1.sort()
arr2.sort()

res = sum(map(lambda x,y : abs(int(x)-int(y)), arr1, arr2 ))
print(res)