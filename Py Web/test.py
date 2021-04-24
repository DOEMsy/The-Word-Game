from random import choice

def test(*a):
    res = 0
    for i in a:
        res += i
    return res

print(test(*3*[1,2]))