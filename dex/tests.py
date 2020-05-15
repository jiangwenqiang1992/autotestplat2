import random
from time import sleep

class test_task:
    i = 1

test = [test_task() for i in range(10)]

print(test[5].i)