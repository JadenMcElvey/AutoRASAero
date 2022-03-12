#!/usr/bin/env python
# coding: utf-8

# # Fin Optimization Using a Genetic Algorithm

# **THIS NOTEBOOK IS IDENTICAL TO THE ORIGINAL EXCEPT THAT THE BOOSTER AND SUSTAINER FIN PARAMETERS ARE CHANGED INDEPENDENTLY FOR EACH FIN CANDIDATE**
# ## Intro
# The goal of this notebook is to optimize fin parameters and ignition delay by using a genetic algorithm. A [genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm) is an algorithmic approach to optimization based largely on the concept of natural selection. The algorithm creates sets of solutions, called generations, and uses the quality of those solutions to inform new candidate solutions. At a high level the steps of the algorithm are as follows.
# 1. Create the first generation by randomly generating a set of candidate solutions
# 2. Evaluate the fitness of all solutions in the generation
# 3. Create the new generation  
#     a. Create offspring candidates by crossing the parameters of previously good solutions  
#     b. Create more solutions by mutating the offspring candidates  
# 4. Repeat steps 2 and 3 for multiple generations to continue optimizing

# ## Setup
# Begin by importing the necessary libraries. Scypi and Numpy are used to create mutated parameters along a truncated normal distribution. Pathlib and Sys are used to deal with file paths and import the RASAero automation code. CSV is used to write the output to a csv file for later analysis in excel.

# In[ ]:


# Genetic Algorithm Imports
from scipy.stats import truncnorm
import numpy as np
import matplotlib.pyplot as plt

# RASAero Automation Imports
import pywinauto
import pathlib
import sys
import time
sys.path.append("..")
from Automation.AutoRASAero import AutoRASAero

# Import to Output csv
import csv

# Global Var
letters = [char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


# ## Defining a Fin Candidate
# A fin candidate is a set of fin dimensions and ignition delay values. Each fin candidate is a possible solution that is evaluated based on its stability and apogee. Most of the code in this class just stores values and provides functions to easily create new candidate solutions.
# ### Crossover and Mutation
# The hallmarks of a genetic algorithm is the use of crossover and mutation techniques. For fin candidates crossover is achieved by taking two parent candidates and averaging the values of each parameter. Mutation is achieved by taking another candidate and randomly sampling from a normal distribution(truncated within valid ranges) centered on the parameters of the parent. This means that it is likely that the mutated parameter will be similar to the parameter of the parent but it is also possible that mutated parameters may differ greatly from that of the "parent".
# ### Fitness
# The most important function in this class is fitness function. The fitness function is the crux of the genetic algorithm. A higher value from the fitness function indicates a better quality solution to the algorithm. A bad fitness function will result in an algorithm that does not optimize solutions. Here the goal is to optimize apogee within the bounds of acceptable stability. To that end the fitness function is as follows. Any candidate solution that results in a global minimum stability below 2 is considered unfit for flight and has a fitness of zero. For candidate solutions with minimum stability over this threshold the fitness is equal to the apogee, with one exception. A maximum global stability over 6 is considered potentially over stable and applies a penalty to the fitness function of 1% per tenth over 6. For instance a maximum stability margin of 6.5 applies a 5% penalty to the apogee when calculating fitness. This function will hopefully optimize the parameters for apogee with appropriate incentives for maintaining stability, but only time will tell.

# In[ ]:


class finCandidate:
    
    rootChordRange = (6, 14)
    spanRange = (6, 6.01)
    tipChordRange = (3, 6)
    sweepRange = (3, 9)
    ignitionDelayRange = (4, 30)
    
    normScale = 2
    
    def __init__(self, gen, boosterParameters, sustainerParameters, ignitionDelay):
        self.gen = gen
        self.genID = "?"
        self.bParams = boosterParameters
        self.sParams = sustainerParameters
        self.ignitionDelay = ignitionDelay
        self.results = None
        
    def __str__(self):
        genStr = "Fin-" + str(self.gen) + "-" + self.genID + "|"
        fitnessStr = "Fitness:" + str(round(self.fitness())) + "|"
        bParamStr = "B_" + "_".join(str(x) for x in self.bParams) + "|"
        sParamStr = "S_" + "_".join(str(x) for x in self.sParams) + "|"
        iDelayStr = "I_" + str(self.ignitionDelay)
        return genStr + fitnessStr + bParamStr + sParamStr + iDelayStr
    
    def toCSV(self):
        csvList = []

        # Append generation string
        csvList.append("Fin-" + str(candidate.gen) + "-" + candidate.genID)
        # Append fitness
        csvList.append(str(round(candidate.fitness())))
        # Append booster parameters
        csvList.extend(str(x) for x in candidate.bParams)
        # Append sustainer parameters
        csvList.extend(str(x) for x in candidate.sParams)
        # Append ignition delay
        csvList.append(str(candidate.ignitionDelay))
        # Append results
        csvList.extend(str(x) for x in candidate.results)

        return csvList
        
    def __lt__(self, other):
        return self.fitness() < other.fitness()
    
    def __eq__(self, other):
        if not isinstance(other, finCandidate):
            return False
        return self.boosterParams == other.boosterParams and self.sustainerParams == other.sustainerParams
    
    def getFinParameters(self):
        return self.bParams, self.sParams
    
    def getIgnitionDelay(self):
        return self.ignitionDelay
        
    def setGenID(self, genIDStr):
        self.genID = genIDStr
        
    def setResuls(self, results):
        self.results = results
        
    def fitness(self):
        minFitStability = 2
        maxFitStability = 6
        
        if not self.verify():
            return 0
        elif self.results == None or self.results[4] < minFitStability:
            return 0
            
        scalar = 1 - (pow(1.35, self.results[5]-maxFitStability) - 1)
        scalar = 0 if scalar < 0 else 1 if scalar > 1 else scalar
        
        fitness = self.results[6] * scalar
        
        return fitness
    
    def verify(self):
        return self._verifyFinParamList(self.bParams) and self._verifyFinParamList(self.sParams)

    def _verifyFinParamList(self, params):
        sweep = params[3]
        tipChord = params[2]
        sweepPlusTipChord = sweep + tipChord
        rootChord = params[0]
        if (sweepPlusTipChord <= (rootChord * 2 / 3) or rootChord < sweepPlusTipChord):
            return False
        else:
            return True
    
    def cross(self, other):
        childBoosterParams = []
        for i in range(4):
            param = round((self.bParams[i] + other.bParams[i]) / 2, 1)
            childBoosterParams.append(param)
        
        childSustainerParams = []
        for i in range(4):
            param = round((self.sParams[i] + other.sParams[i]) / 2, 1)
            childSustainerParams.append(param)

        childIgnitionDelay = round((self.ignitionDelay + other.ignitionDelay) / 2, 1)
        return finCandidate(self.gen + 1, childBoosterParams, childSustainerParams, childIgnitionDelay)
    
    def mutatedCopy(self):
        mutatedBoosterParams = self._mutateParamList(self.bParams)
        mutatedSustainerParams = self._mutateParamList(self.sParams)
        mutatedIgnitionDelay = self._mutateParam(self.ignitionDelay, finCandidate.ignitionDelayRange)
        return finCandidate(self.gen, mutatedBoosterParams, mutatedSustainerParams, mutatedIgnitionDelay)

    def _mutateParamList(self, paramList):
        mutatedRootChord = self._mutateParam(paramList[0], finCandidate.rootChordRange)
        mutatedSpan = self._mutateParam(paramList[1], finCandidate.spanRange)
        mutatedTipChord = self._mutateParam(paramList[2], finCandidate.tipChordRange)
        mutatedSweep = self._mutateParam(paramList[3], finCandidate.sweepRange)
        return [mutatedRootChord, mutatedSpan, mutatedTipChord, mutatedSweep]
    
    def _mutateParam(self, param, paramRange):
        normLowerBound = (paramRange[0] - param) / finCandidate.normScale
        normUpperBound = (paramRange[1] - param) / finCandidate.normScale
        mutatedParam = truncnorm.rvs(normLowerBound, normUpperBound, scale=finCandidate.normScale, loc=param, size=1)
        mutatedParam = mutatedParam.round(1)
        return mutatedParam[0]


# ## Creating Generation Zero
# 
# Generation zero will be the first generation for the genetic algorithm. All the candidates in generation zero are created by randomly sampling parameters from a uniform distribution.

# In[ ]:


rand = np.random.default_rng()
gen = []

while len(gen) < 20:
    finParams = []
    for i in range(2):
        rootChord = rand.uniform(finCandidate.rootChordRange[0], finCandidate.rootChordRange[1])
        rootChord = round(rootChord, 1)
        span = rand.uniform(finCandidate.spanRange[0], finCandidate.spanRange[1])
        span = round(span, 1)
        tipChord = rand.uniform(finCandidate.tipChordRange[0], finCandidate.tipChordRange[1])
        tipChord = round(tipChord, 1)
        sweep = rand.uniform(finCandidate.sweepRange[0], finCandidate.sweepRange[1])
        sweep = round(tipChord, 1)
        finParams.append([rootChord, span, tipChord, sweep])
    
    ignitionDelay = rand.uniform(finCandidate.ignitionDelayRange[0], finCandidate.ignitionDelayRange[1])
    ignitionDelay = round(ignitionDelay)

    candidate = finCandidate(0, finParams[0], finParams[1], ignitionDelay)

    if not candidate.verify():
        continue
    else:
        gen.append(candidate)
        letterIndex = len(gen) - 1
        gen[letterIndex].setGenID(letters[letterIndex])


# ## Iteration
# Now evaluate the fitness of generation zero and create new generations via crossover and mutation. Store each generation in the allGenerations list for later.

# In[ ]:


# Get paths for rocket files and where to save the csv
cwd = str(pathlib.Path.cwd().parent)
# CDX1_FILE = cwd + r"\Resources\MBS_43.CDX1"
CDX1_FILE = cwd + r"\Resources\MBSTemplate2.CDX1"
ENG_FILE = cwd + r"\Resources\TCIMC3_(9899.7771)_5_5_2.329_11.0789_2.eng"
csvPath = cwd + "\\Temp\\"

# Create an object to run the simulations
finSim = AutoRASAero()
# Set the paths for the simulations
finSim.setPaths(CDX1_FILE, ENG_FILE, csvPath)

# Evaluate generation zero
for candidate in gen:
    finSim.startupRASAero()
    boosterFinParams, sustainerFinParams = candidate.getFinParameters()
    candidate.results = finSim.runStabilitySimulation(boosterFinParams, sustainerFinParams, candidate.getIgnitionDelay())
    finSim.closeRASAero()

# Output the best of gen zero
gen.sort(reverse=True)
print("Best:", gen[0])

# Repeatedly create new gens by crossing and mutating
allGenerations = []
allGenerations.append(gen)
lastGen = gen
newGen = []
for i in range(55):
    letterIndex = 0
    for candidateIndex1 in range(5):
        for candidateIndex2 in range(candidateIndex1+1, 5):
            offSpring = lastGen[candidateIndex1].cross(lastGen[candidateIndex2])
            offSpring.setGenID(letters[letterIndex])
            if offSpring.verify():
                newGen.append(offSpring)
                letterIndex += 1

    mutatedIndex = 0
    while len(newGen) < 20:
        mutatedOffspring = newGen[mutatedIndex].mutatedCopy()
        mutatedOffspring.setGenID(letters[letterIndex])
        if mutatedOffspring.verify():
            newGen.append(mutatedOffspring)
            letterIndex += 1
            mutatedIndex += 1
    
    for candidate in newGen:
        successfulSim = False
        while not successfulSim:
            try:
                finSim.startupRASAero()
                boosterFinParams, sustainerFinParams = candidate.getFinParameters()
                candidate.results = finSim.runStabilitySimulation(boosterFinParams, sustainerFinParams, candidate.getIgnitionDelay())
                finSim.closeRASAero()
                successfulSim = True
            except (TimeoutError, pywinauto.ElementNotFoundError):
                pass

    # Output best of this gen and update lastGen
    newGen.sort(reverse=True)
    print("Best:", newGen[0])
    allGenerations.append(newGen)
    lastGen = newGen
    newGen = []

print("Done!")


# ## Output
# Create a new csv file and write the parameter and simulation results of each fin to this file.

# In[ ]:


flatAllGenerations = [candidate for generation in allGenerations for candidate in generation]

outputPath = cwd + "\\Output\\fins.csv"
outputFile = open(outputPath, "w", newline='')

writer = csv.writer(outputFile)
writer.writerow(["Fin Name", "Fitness", "Booster Root Chord", "Booster Span", "Booster Tip Chord", "Booster Sweep", "Sustainer Root Chord", "Sustainer Span", "Sustainer Tip Chord", "Sustainer Sweep", "Ignition Delay", "boosterStartStability", "boosterEndStability", "sustainerStartStability", "sustainerMaxStability", "globalMinStability", "globalMaxStability", "apogee"])

for candidate in flatAllGenerations:
    if candidate.results != None:
        writer.writerow(candidate.toCSV())
        
outputFile.close()


# ## Continued Iteration
# If you want to run more iterations run the block below. Then scroll back up and output the new values to csv.

# In[ ]:


lastGen = allGenerations[-1]
newGen = []
for i in range(1):
    letterIndex = 0
    for candidateIndex1 in range(5):
        for candidateIndex2 in range(candidateIndex1+1, 5):
            offSpring = lastGen[candidateIndex1].cross(lastGen[candidateIndex2])
            offSpring.setGenID(letters[letterIndex])
            if offSpring.verify():
                newGen.append(offSpring)
                letterIndex += 1

    mutatedIndex = 0
    while len(newGen) < 20:
        mutatedOffspring = newGen[mutatedIndex].mutatedCopy()
        mutatedOffspring.setGenID(letters[letterIndex])
        if mutatedOffspring.verify():
            newGen.append(mutatedOffspring)
            letterIndex += 1
            mutatedIndex += 1
    
    for candidate in newGen:
        successfulSim = False
        while not successfulSim:
            try:
                finSim.startupRASAero()
                boosterFinParams, sustainerFinParams = candidate.getFinParameters()
                candidate.results = finSim.runStabilitySimulation(boosterFinParams, sustainerFinParams, candidate.getIgnitionDelay())
                finSim.closeRASAero()
                successfulSim = True
            except (TimeoutError, pywinauto.ElementNotFoundError):
                pass

    # Output best of this gen and update lastGen
    newGen.sort(reverse=True)
    print("Best:", newGen[0])
    allGenerations.append(newGen)
    lastGen = newGen
    newGen = []

print("Done!")

