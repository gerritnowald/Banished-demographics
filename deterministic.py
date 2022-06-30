"""
Simulation of demographic development in Banished

author: Gerrit Nowald
"""

import random
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler

#------------------------------------------------------------------------------
# parameters

parameters = dict(
    Years         = 300 ,   # length of simulation
    InitialAdults = 8  ,
    InitialAge    = 20 ,
    MarryingAge   = 16 ,
    MaxParentAge  = 40 ,
    DyingAge      = 50 ,
    InitialHouses = 4  ,
    HousesPerYear = 1  ,
    MaxHouses     = 100 ,
    HouseCapacity = 5  ,
    AgingPerYear  = 4  ,
    StatsAgeRange = 10 ,    # size of age groups in years for statistics
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
    def __init__(self):
        self.inhabitants = set()

#------------------------------------------------------------------------------
# functions

def findSingles(group):
    return { citizen for citizen in group if citizen.spouse == None 
            and citizen.age >= parameters['MarryingAge'] }


def fillingHouses(houses, population):
    emptyHouses = { house for house in houses if len(house.inhabitants) == 0 }
    
    # marry (if empty house is available)
    singles     = findSingles(population)
    singlewomen = { citizen for citizen in singles if citizen.female }
    for n in range(len(singlewomen)-len(emptyHouses)):
        singlewomen.pop()   # only as much marriages as empty houses
    singlemen = singles - singlewomen
    for woman in singlewomen:
        if len(singlemen) > 0:
            woman.spouse = random.choice(tuple(singlemen))
            woman.spouse.spouse = woman     # update husband's spouse
            singlemen.remove(woman.spouse)
    
    # couples move into empty houses
    marriedMovingWomen = singlewomen - findSingles(singlewomen)
    for woman in marriedMovingWomen:
        if len(emptyHouses) > 0:
            newhouse = random.choice(tuple(emptyHouses))    # 1 house for several citizen
            emptyHouses.remove(newhouse)
            for citizen in {woman, woman.spouse}:
                if citizen.house != None:
                    citizen.house.inhabitants.remove(citizen)   # moving out
                newhouse.inhabitants.add(citizen)               # moving in
                citizen.house = newhouse


def aging(population):  
    for citizen in population:
        citizen.age += parameters['AgingPerYear']
    
    # dying
    dying = {citizen for citizen in population if citizen.age >= parameters['DyingAge']}
    population -= dying
    for citizen in dying:
        if citizen.house != None:
            citizen.house.inhabitants.remove(citizen)
        # if citizen.spouse != None:    # removing spouses leads to re-marrying
        #     citizen.spouse.spouse = None


def offspring(population):
    marriedwomen = { citizen for citizen in population if citizen.female
                    and citizen.spouse != None }
    for woman in marriedwomen:
        if (woman.house == woman.spouse.house 
            and min(woman.age, woman.spouse.age) >= parameters['MarryingAge'] 
            and max(woman.age, woman.spouse.age) <= parameters['MaxParentAge'] 
            and len(woman.house.inhabitants)     <  parameters['HouseCapacity']):
                Newborn = human()
                population.add(Newborn)
                Newborn.house = woman.house
                woman.house.inhabitants.add(Newborn)


def getStatistics(population, houses):
    ageList = [ citizen.age for citizen in population ]  
    stats   = dict( citizens = len(population) )
    if stats['citizens'] > 0:
        stats['citizens age groups'] = []
        for age in range(0, parameters['DyingAge'], parameters['StatsAgeRange'] ):
            stats['citizens age groups'].append( len( { citizen for citizen in population 
                  if  citizen.age >= age 
                  and citizen.age <  age + parameters['StatsAgeRange'] } ) )
        stats['ratio females']    = round( len( { citizen for citizen in population if citizen.female } ) / stats['citizens'] , 2)
        stats['average age']      = round( sum(ageList) / stats['citizens'] )
        stats['ratio singles']    = round( len( findSingles(population) ) / stats['citizens'], 2)
    else:
        stats['citizens age groups'] = [0 for age in range(0, parameters['DyingAge'], parameters['StatsAgeRange']) ]
        stats['ratio females']    = 0
        stats['average age']      = 0
        stats['ratio singles']    = 0
    if len(houses) > 0:
        stats['mean inhabitants'] = round( sum([ len(house.inhabitants) for house in houses ]) / len(houses) , 1)
    else:
        stats['mean inhabitants'] = 0
    return stats


def plot(value, steps = False, grid = False):
    if steps:
        plt.step(range(len(stats)), [stat[value] for stat in stats], where='post', color='gold')
    else:
        plt.plot(range(len(stats)), [stat[value] for stat in stats], color='gold')
    plt.xlabel('years')
    plt.ylabel(value)
    if grid:
        plt.grid()
    plt.tight_layout()


def plotDemographics(legend = True, grid = False):    
    Demographics = np.zeros([len(stats[-1]['citizens age groups']), len(stats)])
    for n in range(len(stats[-1]['citizens age groups'])):
        Demographics[n,:] = [stat['citizens age groups'][n] for stat in stats]
    
    plt.bar(range(len(stats)), Demographics[0,:], width = 1,
            label = '0-' + str(parameters['StatsAgeRange'] - 1) )
    for n in range(1, len(stats[-1]['citizens age groups'])):
        plt.bar(range(len(stats)), Demographics[n,:], width = 1,
                bottom = sum(Demographics[:n,:]),
                label = str(parameters['StatsAgeRange']*n) + '-' + str(parameters['StatsAgeRange']*(n+1)-1) )
    if legend:
        plt.legend()
    plt.xlabel('years')
    plt.ylabel('citizens')
    if grid:
        plt.grid()
    plt.tight_layout()

#------------------------------------------------------------------------------
# initialisation

houses     = { home() for n in range(parameters['InitialHouses']) }

# population = { human(age = parameters['InitialAge']) for n in range(parameters['InitialAdults']) }
population = { human(age = parameters['InitialAge'], female = bool(n % 2)) for n in range(parameters['InitialAdults']) }
# population = { human(age = parameters['InitialAge'] + random.randint(0,10), female = bool(n % 2)) for n in range(parameters['InitialAdults']) }

#------------------------------------------------------------------------------
# simulation

stats = [ getStatistics(population, houses) ]

for year in range(1, parameters['Years'] + 1):
    
    if len(houses) < parameters['MaxHouses']:
        houses.update( { home() for n in range(parameters['HousesPerYear']) } )
       
    aging(population)
    
    fillingHouses(houses, population)
    
    offspring(population)
    
    stats.append( getStatistics(population, houses) )

#------------------------------------------------------------------------------
#%% results

print(stats[-1])


# for citizen in population:
#     print(str(citizen) + ' lives in ' + str(citizen.house))

# print()

# for house in houses:
#     print(str(house) + ' houses ' + str(house.inhabitants))
#     # for citizen in house.inhabitants:
#     #     print(citizen.female)


plt.close('all')
plt.style.use('dark_background')

plt.figure()

# c = plt.get_cmap('Wistia')
    
# c = plt.get_cmap('tab20c').colors
# plt.rcParams['axes.prop_cycle'] = cycler(color=c)

plt.subplot(221)
plot('citizens')
# plotDemographics(legend = False)

plt.subplot(224)
plot('average age')

plt.subplot(222)
plot('ratio singles')

plt.subplot(223)
plot('mean inhabitants')

plt.show()
# plt.savefig('population.png', transparent=True)