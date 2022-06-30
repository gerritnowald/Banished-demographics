"""
Simulation of demographic development in Banished

author: Gerrit Nowald
"""

import random

import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
# parameters

parameters = dict(
    Years         = 300 ,
    InitialHouses = 50  ,
    InitialAdults = 8  ,
    InitialAge    = 20 ,
    MarryingAge   = 16 ,
    MaxParentAge  = 40 ,
    DyingAge      = 40 ,
    HouseCapacity = 5  ,
    AgingPerYear  = 4  ,
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


def getStatistics(population):
    ageList = [ citizen.age for citizen in population ]
    stats = dict( size = len(population) )
    if stats['size'] > 0:
        stats['ageAverage']    = round(sum( ageList ) / stats['size'])
        stats['femaleRatio']   = round(len( { citizen for citizen in population if citizen.female } ) / stats['size'],2)
        stats['singleRatio']   = round(len( findSingles(population) ) / stats['size'],2)
    else:
        stats['ageAverage']    = 0
        stats['femaleRatio']   = 0
        stats['singleRatio']   = 0        
    return stats

#------------------------------------------------------------------------------
# initialisation

houses     = { home() for n in range(parameters['InitialHouses']) }

# population = { human(age = parameters['InitialAge']) for n in range(parameters['InitialAdults']) }
population = { human(age = parameters['InitialAge'], female = bool(n % 2)) for n in range(parameters['InitialAdults']) }
# population = { human(age = parameters['InitialAge'] + random.randint(0,10), female = bool(n % 2)) for n in range(parameters['InitialAdults']) }

#------------------------------------------------------------------------------
# simulation

stats = [ getStatistics(population) ]

for year in range(1, parameters['Years']+1):
    
    # aging
    for citizen in population:
        citizen.age += parameters['AgingPerYear']
    
    # dying
    dying = {citizen for citizen in population if citizen.age >= parameters['DyingAge']}
    population -= dying
    for citizen in dying:  
        citizen.house.inhabitants.remove(citizen)
        # if citizen.spouse != None:    # removing spouses leads to re-marrying
        #     citizen.spouse.spouse = None
        
    fillingHouses(houses, population)
    
    # offspring
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
    
    stats.append(getStatistics(population))

#------------------------------------------------------------------------------
# results

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
# plt.style.use('seaborn-dark')

plt.figure()

# plt.subplot(311)
plt.step(range(len(stats)), [stat['size'] for stat in stats], where='post', color='gold')
plt.xlabel('years')
plt.ylabel('citizens')
plt.tight_layout()

# plt.subplot(312)
# plt.step(range(len(stats)), [stat['singleRatio'] for stat in stats], where='post', color='gold')
# # plt.xlabel('years')
# plt.ylabel('ratio singles')
# plt.tight_layout()

# plt.subplot(313)
# plt.step(range(len(stats)), [stat['ageAverage'] for stat in stats], where='post', color='gold')
# plt.xlabel('years')
# plt.ylabel('average age')
# plt.tight_layout()

plt.show()
# plt.savefig('population.png', transparent=True)