from random import choice

class test(object):
    def __init__(self):
        self.value = 5
    def fun_a(self):
        self.value-=1

    def __str__(self):
        return str(self.value)

a = {5:test(),3:test()}
k = choice(list(a.values()))
k.fun_a()
print(a[5].value,a[3].value)