"""
Simulation of demographic development in Banished

author: Gerrit Nowald
"""

import random

# import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
# parameters

parameters = dict(
    Years         = 60 ,
    InitialAdults = 4  ,
    InitialAge    = 20 ,
    AgingPerYear  = 1  ,
    DyingAge      = 80 ,
    InitialHouses = 2
    )

#------------------------------------------------------------------------------
# classes

class human():
    def __init__(self, age = 0, female = bool(random.randint(0,1)) ):
        self.age    = age
        self.female = female
        self.house  = None

class home():
    def __init__(self, capacity = 5):
        self.capacity = capacity
        self.inhabitants = set()

#------------------------------------------------------------------------------
# functions

def getStatistics(population):
    stats = dict(
        size       = len(population) ,
        femaleList = [ citizen.female for citizen in population ] ,
        ageList    = [ citizen.age    for citizen in population ] ,
    )
    if stats['size'] > 0:
        stats['femaleRatio'] = sum(stats['femaleList']) / stats['size']
        stats['ageAverage']  = sum(stats['ageList'])    / stats['size']
    else:
        stats['femaleRatio'] = 0
        stats['ageAverage']  = None
    return stats

#------------------------------------------------------------------------------
# initialisation

population = { human(age = parameters['InitialAge'], female = bool(n % 2)) for n in range(parameters['InitialAdults']) }
# population = { human(age = parameters['InitialAge'] + random.randint(0,10), female = bool(n % 2)) for n in range(parameters['InitialAdults']) }
houses     = { home() for n in range(parameters['InitialHouses']) }

#------------------------------------------------------------------------------
# simulation

# stats = [getStatistics(population)]

# for year in range(1, parameters['Years']+1):
    
#     # aging
#     for citizen in population:
#         citizen.age += parameters['AgingPerYear']
    
#     # dying
#     population -= {citizen for citizen in population if citizen.age >= parameters['DyingAge']}
    
#     stats.append(getStatistics(population))


homeless    = {citizen for citizen in population if citizen.house == None}
emptyHouses = {house for house in houses if len(house.inhabitants) == 0}

for hobo in homeless:
    if len(emptyHouses) > 0:
        newHouse = random.choice(tuple(emptyHouses))
        newHouse.inhabitants.add(hobo)
        hobo.house = newHouse
        emptyHouses.remove(newHouse)


for citizen in population:
    print(str(citizen.house) + str(citizen))

print()

for house in houses:
    print(str(house) + str(house.inhabitants))
    # for citizen in house.inhabitants:
    #     print(citizen.female)

#------------------------------------------------------------------------------
# plot

# plt.step(range(len(stats)), [stat['size'] for stat in stats], where='post')