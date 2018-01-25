#!/usr/bin/python
from random import randint
import numpy as np
import time

cityamount = int(raw_input("How many nodes?\n"))

graph = np.random.randint(0,2,(cityamount,cityamount))
#graph = (g + g.T)/2
for x in range(0, len(graph)-1):
	for y in range(0, len(graph)-1):
		if (graph[x][y] == 1): 
			graph[x][y] = 0
		elif (graph[x][y] == 0):
			graph[x][y] = 1

def make_graph():
	graph = [[0,1,0,1,1,0,0,0],[1,0,1,0,0,0,1,0],[0,1,0,0,1,0,0,1],[1,0,0,0,0,1,1,0],[1,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,1,0,1,0,0,0,1],[0,0,1,0,0,0,1,0]]
	return graph

def make_population(length, colors):
	population = [[colors[randint(0,2)] for x in range(length)] for y in range(100)]
	return population


def calculate_fitness(population, graph, length):
	fitness = 0
	fitnesslist = [0 for x in range(100)]
	for k in range(100):	
		for x in range(length):
			for y in range(length):
				if(y > x):
					if(graph[x][y] == 1):
						if (population[k][x] != population[k][y]):
							fitness+=1
		fitnesslist[k] = fitness
		fitness=0
	return fitnesslist	

def sort_population(fitnesslist, population, length):
	sortedfitnesindex = sorted(range(len(fitnesslist)), key=lambda k: fitnesslist[k], reverse=True)
	sortedpopulation = [[0 for x in range(length)] for y in range(100)]
	for x in range(50):	
		for y in range(length):
			sortedpopulation[x][y] = population[sortedfitnesindex[x]][y]
	return sortedpopulation

def reproduction(sortedpopulation, colors, mutationfactor):
	for x in range(49):
		firstchild = list(sortedpopulation[randint(0,49)])
		secondchild = list(sortedpopulation[randint(0,49)])
		childCopy = list(secondchild)
		chromo1 = randint(0, len(firstchild))
		chromo2 = randint(0, len(firstchild))

		if (chromo1 == chromo2):
			while (chromo1 == chromo2):
				chromo2 = randint(0, len(firstchild))

		if (chromo1 < chromo2):
			for y in range (chromo1, chromo2):
				secondchild[y] = firstchild[y]
				firstchild[y] = childCopy[y]
		else:
			for y in range (chromo2, chromo1):
				secondchild[y] = firstchild[y]
				firstchild[y] = childCopy[y]

		if(randint(0,10) >= mutationfactor):
			mutationindex = randint(0,len(firstchild)-1)
			mutationcolor = colors[randint(0,2)]
			while (mutationcolor == firstchild[mutationindex]):
				mutationcolor = colors[randint(0,2)]
			firstchild[mutationindex]=mutationcolor

		elif(randint(0,10) >= mutationfactor):
			mutationindex = randint(0,len(secondchild)-1)
			mutationcolor = colors[randint(0,2)]
			while (mutationcolor == secondchild[mutationindex]):
				mutationcolor = colors[randint(0,2)]
			firstchild[mutationindex]=mutationcolor

		sortedpopulation[x+50] = firstchild
		sortedpopulation[x+51] = secondchild

	return sortedpopulation

def find_optimal(graph):
	connections = 0
	for x in range(length):
			for y in range(length):
				if(y > x):
					if(graph[x][y] == 1):
						connections +=1
	return connections

# 0 is Black, 1 is White and 2 is Red
colors = ["B","W","R"]
#graph = make_graph()
length = len(graph)
mutationfactor = int(raw_input("from 1 to 10 how often are mutations accepted?\n"))
start = time.time()
population = make_population(length, colors)
optimal = int(find_optimal(graph))
iterations = 500
#int(raw_input("how many iterations before stop?")) 
rounds = 0
improvementcounter = 0
oldfitnesslist = calculate_fitness(population, graph, length)

while(rounds < iterations):
	fitnesslist = calculate_fitness(population, graph, length)
	if(oldfitnesslist[0]!=fitnesslist[0]):
		improvementcounter = 0
	oldfitnesslist = list(fitnesslist)
	sortedpopulation = sort_population(fitnesslist, population, length)
	offspring = reproduction(sortedpopulation, colors, mutationfactor)
	population = list(offspring)
	if (int(fitnesslist[0])==optimal):
		break
	rounds += 1
	improvementcounter += 1



#aftersort = sorted(calculate_fitness(offspring, graph, length), reverse=True)

#counter = 0
#for x in range(100):
#	for y in range(length):
#		print population[x][y]
#		if(y == length-1):
#			print "\n"
#			counter += 1

#for x in range(len(fitnesslist)):
#		print aftersort[x]

end = time.time()
print graph
print "Worst solution is: " +str(optimal)
print "optimalsolution found after: " +str(rounds-improvementcounter) + " generations with fitness of: " + str(optimal-fitnesslist[0]) + " after " + str(end - start) + " seconds"
print population[0] 
print "iterations without improvement = " + str(improvementcounter)
