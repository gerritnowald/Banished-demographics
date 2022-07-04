# -*- coding: utf-8 -*-
"""
Simulation of demographic development in Banished

author: Gerrit Nowald
"""

import classes
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
# parameters

parameters = dict(
    Years         = 100 ,   # length of simulation
    InitialAdults = 8  ,
    InitialAge    = 20 ,
    MarryingAge   = 16 ,
    MaxParentAge  = 40 ,
    DyingAge      = 80 ,
    InitialHouses = 4  ,
    HousesPerYear = 1  ,
    MaxHouses     = 50 ,
    HouseCapacity = 5  ,
    AgingPerYear  = 4  ,
    StatsAgeRange = 17 ,    # size of age groups in years for statistics
    Random        = False   # randomness for sex and start age
    )

#------------------------------------------------------------------------------
# initialisation

population = classes.population(parameters)

village    = classes.village(parameters)

#------------------------------------------------------------------------------
# simulation

statsPopulation = []
statsHouses     = []

for year in range(1, parameters['Years'] + 1):

    village.build()

    population.aging()

    village.fillingHouses(population)

    population.offspring()

    statsPopulation.append( population.getStatistics() )
    statsHouses.append(        village.getStatistics() )

#------------------------------------------------------------------------------
#%% results

print( statsPopulation[-1] )
print( statsHouses[-1] )


plt.close('all')
plt.style.use('dark_background')

classes.plotResult(parameters, statsPopulation, statsHouses)

plt.show()
# plt.savefig('result_deterministic.png', transparent=False)
