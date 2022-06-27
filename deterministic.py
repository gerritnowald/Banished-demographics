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
    InitialAdults = 8  ,
    InitialAge    = 20 ,
    AgingPerYear  = 1  ,
    DyingAge      = 80
    )

#------------------------------------------------------------------------------
# classes

class human():
    def __init__(self, age=0, female=None):
        self.age    = age
        self.female = female
        if female == None:
            # define sex randomly
            if random.randint(0,1) == 0:
                self.female = True
            else:
                self.female = False

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

#------------------------------------------------------------------------------
# initialisation

population = set()
for citizenNumber in range(parameters['InitialAdults']):
    # define sex alternating
    if citizenNumber % 2 == 0:
        female = True
    else:
        female = False
    # add new citizen 
    population.add( human(age = parameters['InitialAge'] + random.randint(0,20), female = female) )

#------------------------------------------------------------------------------
# simulation

sizeVec = []
for year in range(1, parameters['Years']+1):
    dying = set()
    for citizen in population:
        citizen.age += parameters['AgingPerYear']
        if citizen.age >= parameters['DyingAge']:
            dying.add(citizen)
    population -= dying
    statistics = getStatistics(population)
    sizeVec.append(statistics['size'])

#------------------------------------------------------------------------------
# plot

plt.plot(sizeVec)