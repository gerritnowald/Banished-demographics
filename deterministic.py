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
    def __init__(self, age=0, female=None):
        self.age    = age
        self.female = female
        if female == None:
            if random.randint(0,1) == 0:
                self.female = True
            else:
                self.female = False
        self.house = None

class home():
    def __init__(self, capacity = 5):
        self.capacity = capacity
        self.inhabitants = set()

#------------------------------------------------------------------------------
# functions

def getStatistics(population):
    statistics = dict(
        size       = len(population) ,
        femaleList = [ citizen.female for citizen in population ] ,
        ageList    = [ citizen.age    for citizen in population ] ,
    )
    if statistics['size'] > 0:
        statistics['femaleRatio'] = sum(statistics['femaleList'])/statistics['size']
        statistics['ageAverage']  = sum(statistics['ageList'])/len(statistics['ageList'])
    else:
        statistics['femaleRatio'] = 0
        statistics['ageAverage']  = None
    return statistics

def createPopulation(parameters):
    population = set()
    for citizenNumber in range(parameters['InitialAdults']):
        if citizenNumber % 2 == 0:
            female = True
        else:
            female = False
        population.add( human(age = parameters['InitialAge'], female = female) )
        # population.add( human(age = parameters['InitialAge'] + random.randint(0,10), female = female) )
    return population

def createHouses(parameters):
    houses = set()
    for houseNumber in range(parameters['InitialHouses']):
        houses.add( home() )
    return houses

def findEmptyHouses(houses, inhabitants = 0):
    emptyHouses = set()
    for house in houses:
        if len(house.inhabitants) == inhabitants:
            emptyHouses.add(house)
    return emptyHouses

def findHomeless(population):
    homeless = set()
    for citizen in population:
        if citizen.house == None:
            homeless.add(citizen)
    return homeless

#------------------------------------------------------------------------------
# initialisation

population = createPopulation(parameters)
houses     = createHouses(parameters)

#------------------------------------------------------------------------------
# simulation

# statistics = [getStatistics(population)]

# for year in range(1, parameters['Years']+1):
    
#     # aging & dying
#     dying = set()
#     for citizen in population:
#         citizen.age += parameters['AgingPerYear']
#         if citizen.age >= parameters['DyingAge']:
#             dying.add(citizen)
#     population -= dying
    
#     statistics.append(getStatistics(population))



emptyHouses = findEmptyHouses(houses)
homeless    = findHomeless(population)

for hobo in homeless:
    if len(emptyHouses) > 0:
        newHouse = random.choice(tuple(emptyHouses))
        newHouse.inhabitants.add(hobo)
        hobo.house = newHouse
        emptyHouses.remove(newHouse)


# for citizen in population:
#     print(citizen.house)

# for house in houses:
#     print(house.inhabitants)
#     # for citizen in house.inhabitants:
#     #     print(citizen.female)

#------------------------------------------------------------------------------
# plot

# plt.step(range(len(statistics)), 
#           [statistic['size'] for statistic in statistics], where='post')