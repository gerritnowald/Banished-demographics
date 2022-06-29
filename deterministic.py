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
    Years         = 55 ,
    InitialHouses = 2  ,
    InitialAdults = 3  ,
    InitialAge    = 20 ,
    MarryingAge   = 16 ,
    MaxParentAge  = 40 ,
    DyingAge      = 80 ,
    AgingPerYear  = 1  ,
    )

#------------------------------------------------------------------------------
# classes

class human():
    def __init__(self, age = 0, female = None ):
        self.age    = age
        if female == None:
            female = bool(random.randint(0,1))  # random default does not work
        self.female = female
        self.house  = None
        self.spouse = None

class home():
    def __init__(self, capacity = 5):
        self.capacity = capacity
        self.inhabitants = set()

#------------------------------------------------------------------------------
# functions

def findWomen(group):
    return { citizen for citizen in group if citizen.female }

def findSingles(group):
    return { citizen for citizen in group if citizen.spouse == None 
            and citizen.age >= parameters['MarryingAge'] }

def findHomeless(group):
    return { citizen for citizen in group if citizen.house == None}

def moving(newhouse, group):
    for citizen in group:
        if citizen.house != None:
            citizen.house.inhabitants.remove(citizen)   # moving out
        newhouse.inhabitants.add(citizen)               # moving in
        citizen.house = newhouse


def fillingHouses(houses, population):

    emptyHouses = { house for house in houses if len(house.inhabitants) == 0 }
    singles     = findSingles(population)
    singlewomen = findWomen(singles)
    
    for n in range(len(singlewomen)-len(emptyHouses)):
        singlewomen.pop()   # only as much marriages as empty houses
    
    # marry
    singlemen = singles - singlewomen
    for woman in singlewomen:
        if len(singlemen) > 0:
            woman.spouse = random.choice(tuple(singlemen))
            woman.spouse.spouse = woman
            singlemen.remove(woman.spouse)
    
    # couples move into empty houses
    marriedMovingWomen = singlewomen - findSingles(singlewomen)
    for woman in marriedMovingWomen:
        if len(emptyHouses) > 0:
            newhouse = random.choice(tuple(emptyHouses))
            moving(newhouse, {woman, woman.spouse})
            emptyHouses.remove(newhouse)
    
    # homeless move into empty houses
    homeless = findHomeless(population)
    for hobo in homeless:
        if len(emptyHouses) > 0:
            newhouse = random.choice(tuple(emptyHouses))
            moving(newhouse, {hobo})
            emptyHouses.remove(hobo.house)


def getStatistics(population):
    stats = dict(
        size    = len(population) ,
        ageList = [ citizen.age for citizen in population ] ,
    )
    if stats['size'] > 0:
        stats['ageAverage']    = sum(stats['ageList']) / stats['size']
        stats['femaleRatio']   = len( findWomen(population) )   / stats['size']
        stats['singleRatio']   = len( findSingles(population) ) / stats['size']
        stats['homelessRatio'] = len( findHomeless(population) ) / stats['size']
    else:
        stats['ageAverage']    = None
        stats['femaleRatio']   = 0
        stats['singleRatio']   = 0
        stats['homelessRatio'] = 0
        
    return stats

#------------------------------------------------------------------------------
# initialisation

houses     = { home() for n in range(parameters['InitialHouses']) }

# population = { human(age = parameters['InitialAge']) for n in range(parameters['InitialAdults']) }
population = { human(age = parameters['InitialAge'], female = bool(n % 2)) for n in range(parameters['InitialAdults']) }
# population = { human(age = parameters['InitialAge'] + random.randint(0,10), female = bool(n % 2)) for n in range(parameters['InitialAdults']) }

fillingHouses(houses, population)

#------------------------------------------------------------------------------
# simulation









stats = [getStatistics(population)]

# for year in range(1, parameters['Years']+1):
    
#     # aging
#     for citizen in population:
#         citizen.age += parameters['AgingPerYear']
    
#     # dying
#     dying = {citizen for citizen in population if citizen.age >= parameters['DyingAge']}
#     population -= dying
#     for citizen in dying:
#         citizen.house.inhabitants.remove(citizen)
#         # if citizen.spouse != None:    # removing spouses leads to re-marrying
#         #     citizen.spouse.spouse = None
    
#     stats.append(getStatistics(population))


for citizen in population:
    print(str(citizen) + ' lives in ' + str(citizen.house))

print()

for house in houses:
    print(str(house) + ' houses ' + str(house.inhabitants))
    # for citizen in house.inhabitants:
    #     print(citizen.female)

#------------------------------------------------------------------------------
# plot

# plt.step(range(len(stats)), [stat['size'] for stat in stats], where='post')