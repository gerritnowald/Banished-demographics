"""
Simulation of demographic development in Banished

author: Gerrit Nowald
"""

import random

#------------------------------------------------------------------------------
# parameters

parameters = dict(
    InitialPopulation = 8 ,
    InitialAge        = 20
    )

#------------------------------------------------------------------------------
# classes

class citizen():
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

def createPopulation(parameters):
    population = set()
    for n in range(parameters['InitialPopulation']):
        # define sex alternating
        if n % 2 == 0:
            female = True
        else:
            female = False
        # add new citizen 
        population.add( citizen(age = parameters['InitialAge'], female = female) )
    return population

def getStatistics(population):
    statistics = dict(
        size       = len(population) ,
        femaleList = [ citizen.female for citizen in population ] ,
        ageList    = [ citizen.age    for citizen in population ] ,
    )
    statistics['femaleRatio'] = sum(statistics['femaleList'])/statistics['size']
    statistics['ageAverage']  = sum(statistics['ageList'])/len(statistics['ageList'])
    return statistics

#------------------------------------------------------------------------------
# create start population

population = createPopulation(parameters)

#------------------------------------------------------------------------------
# probe population statistics

statistics = getStatistics(population)