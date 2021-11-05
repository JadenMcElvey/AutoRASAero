#!/usr/bin/env python
# coding: utf-8

# # Fin Optimization Using a Genetic Algorithm

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
    
    rootChordRange = (8, 16)
    spanRange = (6, 8)
    tipChordRange = (1, 9)
    sweepRange = (4, 12)
    ignitionDelayRange = (4, 30)
    
    normScale = 2
    
    def __init__(self, gen, parameters):
        self.gen = gen
        self.genID = "?"
        self.rootChord = parameters[0]
        self.span = parameters[1]
        self.tipChord = parameters[2]
        self.sweep = parameters[3]
        self.ignitionDelay = parameters[4]
        self.results = None
        
    def __str__(self):
        genStr = "Fin-" + str(self.gen) + "-" + self.genID + "|"
        fitnessStr = "Fitness:" + str(round(self.fitness())) + "|"
        paramStr = "_".join(str(x) for x in [self.rootChord, self.span, self.tipChord, self.sweep, self.ignitionDelay])
        return genStr + fitnessStr + paramStr
    
    def toCSV(self):
        genStr = "Fin-" + str(self.gen) + "-" + self.genID + ","
        fitnessStr = str(round(self.fitness())) + ","
        paramStr = ",".join(str(x) for x in [self.rootChord, self.span, self.tipChord, self.sweep, self.ignitionDelay]) + ","
        resultStr = ",".join(str(x) for x in self.results)
        csvString = genStr + fitnessStr + paramStr + resultStr
        return csvString.split(",")
        
    def __lt__(self, other):
        return self.fitness() < other.fitness()
    
    def __eq__(self, other):
        if not isinstance(other, finCandidate):
            return False
        sameRootChord = self.rootChord == other.rootChord
        sameSpan = self.span == other.span
        sameTipChord = self.tipChord == other.tipChord
        sameSweep = self.sweep == other.sweep
        sameIgnitionDelay = self.ignitionDelay == other.ignitionDelay
        return sameRootChord and sameSpan and sameTipChord and sameSweep and sameIgnitionDelay
    
    def getFinParameters(self):
        return (self.rootChord, self.span, self.tipChord, self.sweep)
    
    def getIgnitionDelay(self):
        return self.ignitionDelay
        
    def setGenID(self, genIDStr):
        self.genID = genIDStr
        
    def setResuls(self, results):
        self.results = results
        
    def fitness(self):
        minFitStability = 2
        
        if not self.verify():
            return 0
        elif self.results == None or self.results[4] < minFitStability:
            return 0
            
        scalar = 1 - (pow(1.35, self.results[5]-6) - 1)
        scalar = 0 if scalar < 0 else 1 if scalar > 1 else scalar
        
        fitness = self.results[6] * scalar
        
        return fitness
    
    def verify(self):
        sweepPlusTipChord = self.sweep + self.tipChord
        if (sweepPlusTipChord <= (self.rootChord * 2 / 3) or self.rootChord < sweepPlusTipChord):
            return False
        else:
            return True
    
    def cross(self, other):
        childRootChord = round((self.rootChord + other.rootChord) / 2, 1)
        childSpan = round((self.span + other.span) / 2, 1)
        childTipChord = round((self.tipChord + other.tipChord) / 2, 1)
        childSweep = round((self.sweep + other.sweep) / 2, 1)
        childIgnitionDelay = round((self.ignitionDelay + other.ignitionDelay) / 2, 1)
        return finCandidate(self.gen + 1, [childRootChord, childSpan, childTipChord, childSweep, childIgnitionDelay])
    
    def mutatedCopy(self):
        mutatedRootChord = self._mutateParam(self.rootChord, finCandidate.rootChordRange)
        mutatedSpan = self._mutateParam(self.span, finCandidate.spanRange)
        mutatedTipChord = self._mutateParam(self.tipChord, finCandidate.tipChordRange)
        mutatedSweep = self._mutateParam(self.sweep, finCandidate.sweepRange)
        mutatedIgnitionDelay = self._mutateParam(self.ignitionDelay, finCandidate.ignitionDelayRange)
        return finCandidate(self.gen, [mutatedRootChord, mutatedSpan, mutatedTipChord, mutatedSweep, mutatedIgnitionDelay])
    
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
    rootChord = rand.uniform(finCandidate.rootChordRange[0], finCandidate.rootChordRange[1])
    rootChord = round(rootChord)
    span = rand.uniform(finCandidate.spanRange[0], finCandidate.spanRange[1])
    span = round(span, 1)
    tipChord = rand.uniform(finCandidate.tipChordRange[0], finCandidate.tipChordRange[1])
    tipChord = round(tipChord, 1)
    sweep = rand.uniform(finCandidate.sweepRange[0], finCandidate.sweepRange[1])
    sweep = round(tipChord, 1)
    ignitionDelay = rand.uniform(finCandidate.ignitionDelayRange[0], finCandidate.ignitionDelayRange[1])
    ignitionDelay = round(ignitionDelay)
    
    candidate = finCandidate(0, [rootChord, span, tipChord, sweep, ignitionDelay])
    if not candidate.verify():
        continue
    else:
        gen.append(candidate)
        i = len(gen) - 1
        gen[i].setGenID(letters[i])


# ## Iteration
# Now evaluate the fitness of generation zero and create new generations via crossover and mutation. Store each generation in the allGenerations list for later.

# In[ ]:


# Get paths for rocket files and where to save the csv
cwd = str(pathlib.Path.cwd().parent)
CDX1_FILE = cwd + r"\Resources\MBS_43.CDX1"
ENG_FILE = cwd + r"\Resources\TCIMC3_(9899.7771)_5_5_2.329_11.0789_2.eng"
csvPath = cwd + "\\Temp\\"

# Create an object to run the simulations
finSim = AutoRASAero()
# Set the paths for the simulations
finSim.setPaths(CDX1_FILE, ENG_FILE, csvPath)

# Evaluate generation zero
for candidate in gen:
    finSim.startupRASAero()
    finParams = candidate.getFinParameters()
    candidate.results = finSim.runStabilitySimulation(finParams, finParams, candidate.getIgnitionDelay())
    finSim.closeRASAero()

# Output the best of gen zero
gen.sort(reverse=True)
print("Best:", gen[0])

# Repeatedly create new gens by crossing and mutating
allGenerations = []
allGenerations.append(gen)
lastGen = gen
newGen = []
for i in range(2):
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
        finSim.startupRASAero()
        finParams = candidate.getFinParameters()
        candidate.results = finSim.runStabilitySimulation(finParams, finParams, candidate.getIgnitionDelay())
        finSim.closeRASAero()

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
writer.writerow(["Fin Name", "Fitness", "Root Chord", "Span", "Tip Chord", "Sweep", "Ignition Delay", "boosterStartStability", "boosterEndStability", "sustainerStartStability", "sustainerMaxStability", "globalMinStability", "globalMaxStability", "apogee"])

for candidate in flatAllGenerations:
    if candidate.results != None:
        writer.writerow(candidate.toCSV())
        
outputFile.close()


# ## Continued Iteration
# If you want to run more iterations run the block below. Then scroll back up and output the new values to csv.

# In[ ]:


lastGen = allGenerations[-1]
newGen = []
for i in range(8):
    finSim.startupRASAero()
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
        finSim.startupRASAero()
        finParams = candidate.getFinParameters()
        candidate.results = finSim.runStabilitySimulation(finParams, finParams, candidate.getIgnitionDelay())
        finSim.closeRASAero()

    # Output best of this gen and update lastGen
    newGen.sort(reverse=True)
    print("Best:", newGen[0])
    allGenerations.append(newGen)
    lastGen = newGen
    newGen = []

print("Done!")

