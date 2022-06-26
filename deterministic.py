import random

InitialPopulation = 8

class citizen():
    def __init__(self):
        self.age = 0
        if random.randint(0,1) == 0:
            self.female = True

citizens = set()

for n in range(InitialPopulation):
    citizens.add(citizen())