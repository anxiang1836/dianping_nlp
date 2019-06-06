import time
import math

list1 = [[11, 12345], 22, 33, 44, 5555, 444, 5555]
list2 = [1]

print(list1[0][0:2])

for i in range(0, 4):
    print(i)

print(not list1.__contains__(12))
list1.extend(list2)
print(list1)

if __name__ == '__main__':
    x = (2, 2)
    y = (3, 1)

    d = (x[0] * y[0] + x[1] * y[1]) / (math.sqrt(x[0] * x[0] + x[1] * x[1]) * math.sqrt(y[0] * y[0] + y[1] * y[1]))

    print(d)
