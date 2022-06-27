"""
Simulation of demographic development in Banished

author: Gerrit Nowald
"""

import random

#------------------------------------------------------------------------------
# parameters

InitialPopulation = 8
InitialAge = 20

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
# create start population

citizens = set()

for n in range(InitialPopulation):
    # define sex alternating
    if n % 2 == 0:
        female = True
    else:
        female = False
    # add new citizen 
    citizens.add( citizen(age=InitialAge, female=female) )

#------------------------------------------------------------------------------
# 

PopulationFemale = [ citizen.female for citizen in citizens ]