# -*- coding: utf-8 -*-
"""
Simulation of demographic development in Banished

author: Gerrit Nowald
"""

import statistics
import random
import matplotlib.pyplot as plt
import numpy as np

#------------------------------------------------------------------------------
# classes

class population():
    def __init__(self, parameters):
        self.parameters = parameters
        if self.parameters['Random']:
            self.citizens = { self.citizen( age = self.parameters['InitialAge'] + random.randint(0,10) ) for n in range(self.parameters['InitialAdults']) }
        else:
            self.citizens = { self.citizen( age = self.parameters['InitialAge'], female = bool(n % 2) )  for n in range(self.parameters['InitialAdults']) }
            self.femaleSwitch = True
            
    class citizen():
        def __init__(self, age = 0, female = None ):
            self.age    = age
            if female == None:
                female = bool(random.randint(0,1))  # random default initiated only once
            self.female = female
            self.house  = None
            self.spouse = None

    def aging(self):
        for citizen in self.citizens:
            citizen.age += self.parameters['AgingPerYear']
        dying = { citizen for citizen in self.citizens if citizen.age >= self.parameters['DyingAge'] }
        self.citizens -= dying
        for citizen in dying:
            if citizen.house != None:
                citizen.house.inhabitants.remove(citizen)

    def offspring(self):
        marriedwomen = { citizen for citizen in self.citizens if citizen.female
                        and citizen.spouse != None }
        for woman in marriedwomen:
            if ( woman.house == woman.spouse.house
                and min(woman.age, woman.spouse.age) >= self.parameters['MarryingAge']
                and max(woman.age, woman.spouse.age) <= self.parameters['MaxParentAge']
                and len(woman.house.inhabitants)     <  self.parameters['HouseCapacity'] ):
                    if self.parameters['Random']:
                        Newborn = self.citizen()   # sex random
                    else:
                        Newborn = self.citizen(female = self.femaleSwitch)
                        self.femaleSwitch = not self.femaleSwitch     # sex alternating
                    self.citizens.add(Newborn)
                    Newborn.house = woman.house
                    woman.house.inhabitants.add(Newborn)

    def findSingles(self, group = None):
        if group == None:
            group = self.citizens   # self not defined in function call
        return { citizen for citizen in group if citizen.spouse == None
                and citizen.age >= self.parameters['MarryingAge']
                and citizen.age <  self.parameters['MaxParentAge'] }

    def getStatistics(self):
        ageList = [ citizen.age for citizen in self.citizens ]
        stats = {'citizens' : len(self.citizens) }
        if stats['citizens'] > 0:
            stats['citizens age groups'] = []
            for age in range(0, self.parameters['DyingAge'] + 1, self.parameters['StatsAgeRange'] ):
                stats['citizens age groups'].append( len( { citizen for citizen in self.citizens
                      if  citizen.age >= age
                      and citizen.age <  age + self.parameters['StatsAgeRange'] } ) )
            stats['average age']   = round( sum(ageList) / stats['citizens'] )
            stats['median age']    = round( statistics.median(ageList) )
            stats['ratio females'] = round( len( { citizen for citizen in self.citizens if citizen.female } ) / stats['citizens'] , 2)
            stats['ratio singles'] = round( len( self.findSingles() ) / stats['citizens'], 2)
        else:
            stats['citizens age groups'] = [0 for age in range(0, self.parameters['DyingAge']+1, self.parameters['StatsAgeRange']) ]
            stats['average age']   = 0
            stats['median age']    = 0
            stats['ratio females'] = 0
            stats['ratio singles'] = 0
        return stats


class village():
    def __init__(self, parameters):
        self.parameters = parameters
        self.houses = { self.house() for n in range(self.parameters['InitialHouses']) }
    
    class house():
        def __init__(self):
            self.inhabitants = set()

    def build(self):
        if len(self.houses) < self.parameters['MaxHouses']:
            self.houses.update( { self.house() for n in range(self.parameters['HousesPerYear']) } )

    def fillingHouses(self, population):
        emptyHouses = { house for house in self.houses if len(house.inhabitants) == 0 }

        # marry (if empty house is available)
        singles     = population.findSingles()
        singlewomen = { citizen for citizen in singles if citizen.female }
        for n in range(len(singlewomen)-len(emptyHouses)):
            singlewomen.pop()   # only as much marriages as empty houses
        singlemen = singles - singlewomen
        for woman in singlewomen:
            if len(singlemen) > 0:
                woman.spouse = singlemen.pop()
                woman.spouse.spouse = woman     # update husband's spouse

        # couples move into empty houses
        marriedMovingWomen = singlewomen - population.findSingles(group = singlewomen)
        for woman in marriedMovingWomen:
            if len(emptyHouses) > 0:
                newhouse = emptyHouses.pop()    # 1 house for several citizen
                for citizen in {woman, woman.spouse}:
                    if citizen.house != None:
                        citizen.house.inhabitants.remove(citizen)   # moving out
                    newhouse.inhabitants.add(citizen)               # moving in
                    citizen.house = newhouse

    def getStatistics(self):
        if len(self.houses) > 0:
            stats = {'inhabitants groups' : [] }
            for inhabitants in range( self.parameters['HouseCapacity'] + 1 ):
                stats['inhabitants groups'].append( len( { house for house in self.houses
                      if  len(house.inhabitants) >= inhabitants
                      and len(house.inhabitants) <  inhabitants + 1 } ) )
            stats['average inhabitants'] = round( sum([ len(house.inhabitants) for house in self.houses ]) / len(self.houses) , 1)
        else:
            stats['inhabitants groups']  = [0 for inhabitants in range(0, self.parameters['HouseCapacity']) ]
            stats['average inhabitants'] = 0
        return stats

#------------------------------------------------------------------------------
# functions

def plotResult(parameters, statsPopulation, statsHouses):
    fig, (ax1, ax3) = plt.subplots(2, 1, sharex=True)

    years = range(1, len(statsPopulation)+1)


    Demographics = np.zeros([len(statsPopulation[-1]['citizens age groups']), len(statsPopulation)])
    for n in range(len(statsPopulation[-1]['citizens age groups'])):
        Demographics[n,:] = [stat['citizens age groups'][n] for stat in statsPopulation]

    ax1.bar(years, Demographics[0,:], width = 1,
            label = 'aged 0-' + str(parameters['StatsAgeRange'] - 1) )
    for n in range(1, len(statsPopulation[-1]['citizens age groups'])):
        ax1.bar(years, Demographics[n,:], width = 1,
                bottom = sum(Demographics[:n,:]),
                label = 'aged ' + str(parameters['StatsAgeRange']*n) + '-' + str(parameters['StatsAgeRange']*(n+1)-1) )

    ax1.legend(loc='upper left', prop={'size': 6})
    ax1.set_ylabel('citizens')


    ax2 = ax1.twinx()

    ax2.step(years, [stat['median age'] for stat in statsPopulation], where='mid', color='gold')

    ax2.set_ylabel('median age', color='gold')
    ax2.tick_params(axis='y', colors='gold')


    Inhabitants = np.zeros([len(statsHouses[-1]['inhabitants groups']), len(statsHouses)])
    for n in range(len(statsHouses[-1]['inhabitants groups'])):
        Inhabitants[n,:] = [stat['inhabitants groups'][n] for stat in statsHouses]

    ax3.bar(years, Inhabitants[0,:], width = 1, label = 'empty' )
    for n in range(1, len(statsHouses[-1]['inhabitants groups'])-1 ):
        ax3.bar(years, Inhabitants[n,:], width = 1,
                bottom = sum(Inhabitants[:n,:]), label = str(n) + ' inhabitants' )
    ax3.bar(years, Inhabitants[-1,:], width = 1,
            bottom = sum(Inhabitants[:-1,:]), label = 'full' )

    ax3.legend(loc='upper left', prop={'size': 6})
    ax3.set_xlabel('years')
    ax3.set_ylabel('houses')


    ax4 = ax3.twinx()

    ax4.step(years, [stat['ratio singles'] for stat in statsPopulation], where='mid', color='gold')

    ax4.set_ylabel('ratio singles', color='gold')
    ax4.tick_params(axis='y', colors='gold')