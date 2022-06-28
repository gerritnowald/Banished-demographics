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
    InitialHouses = 2  ,
    InitialAdults = 5  ,
    InitialAge    = 20 ,
    MarryingAge   = 16 ,
    MaxParentAge  = 40 ,
    DyingAge      = 80 ,
    AgingPerYear  = 1  ,
    )

#------------------------------------------------------------------------------
# classes

class human():
    def __init__(self, age = 0, female = bool(random.randint(0,1)) ):
        self.age    = age
        self.female = female
        self.house  = None
        self.spouse = None

class home():
    def __init__(self, capacity = 5):
        self.capacity = capacity
        self.inhabitants = set()

#------------------------------------------------------------------------------
# functions

def getStatistics(population):
    stats = dict(
        size    = len(population) ,
        women   = { citizen for citizen in population if citizen.female } ,
        singles = { citizen for citizen in population if citizen.spouse == None 
                   and citizen.age >= parameters['MarryingAge'] } ,
        ageList = [ citizen.age    for citizen in population ] ,
    )
    if stats['size'] > 0:
        stats['femaleRatio'] = len(stats['women'])   / stats['size']
        stats['ageAverage']  = sum(stats['ageList']) / stats['size']
    else:
        stats['femaleRatio'] = 0
        stats['ageAverage']  = None
    return stats

def findSpouses(group):    
    women = { citizen for citizen in group if citizen.female }
    men = population - women
    for woman in women:
        if len(men) > 0:
            woman.spouse = random.choice(tuple(men))
            woman.spouse.spouse = woman
            men.remove(woman.spouse)

#------------------------------------------------------------------------------
# initialisation

houses     = { home() for n in range(parameters['InitialHouses']) }

population = { human(age = parameters['InitialAge'], female = bool(n % 2)) for n in range(parameters['InitialAdults']) }
# population = { human(age = parameters['InitialAge'] + random.randint(0,10), female = bool(n % 2)) for n in range(parameters['InitialAdults']) }

findSpouses(population)

for citizen in population:
    print(str(citizen)+str(citizen.spouse))

#------------------------------------------------------------------------------
# simulation

stats = [getStatistics(population)]

# for year in range(1, parameters['Years']+1):
    
#     # aging
#     for citizen in population:
#         citizen.age += parameters['AgingPerYear']
    
#     # dying
#     population -= {citizen for citizen in population if citizen.age >= parameters['DyingAge']}
    
#     stats.append(getStatistics(population))


# homeless    = {citizen for citizen in population if citizen.house == None}
# emptyHouses = {house for house in houses if len(house.inhabitants) == 0}

# for hobo in homeless:
#     if len(emptyHouses) > 0:
#         newHouse = random.choice(tuple(emptyHouses))
#         newHouse.inhabitants.add(hobo)
#         hobo.house = newHouse
#         emptyHouses.remove(newHouse)



# for citizen in population:
#     print(str(citizen.house) + str(citizen))

# print()

# for house in houses:
#     print(str(house) + str(house.inhabitants))
#     # for citizen in house.inhabitants:
#     #     print(citizen.female)

#------------------------------------------------------------------------------
# plot

# plt.step(range(len(stats)), [stat['size'] for stat in stats], where='post')