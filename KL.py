"""This file will run the KL algorithm and return the best partition"""

#Issues with current build:
#   -the loop to calculate the gains is extremely slow, another method needs to be devised
#   -the D prime values still need to be calculated
#   -the final cut size still needs to be calculated

from __future__ import absolute_import

from functions import *


def main():

    #nodes is the set of vertices (components) from the netlist
    #E is the hyperedge set with corresponding weights for each net
    #modE is the graphical representation of the hyperedge set
    nodes, E, modE = hyperGraph() #this will call the function and obtain desired KL inputs

    partA = []
    partB = []

    #partA and partB are the bi-partitions for the algorithm, here we create the partitions equally and update the partition
    #   indicator in the tuple for the component to indicate which partition it exists in
    x = 0
    for node in nodes:
        if x%2 == 0:
            partB.append(node)
            temp = list(nodes[node])
            temp[3] = "b"
            nodes[node] = tuple(temp)
        else:
            partA.append(node)
        x += 1
    del x

    optPartA = partA #holds the optimal partition A, initializes to partA
    optPartB = partB #holds the optimal parition B, initializes to partB

    print(f'Initial Partition A: {partA}')
    print(f'Initial Partition B: {partB}')

    D = {} #dict used to store D values of components

    for i in range(4): #here we are doing 4 total iterations

        ieCost(nodes, modE) #determine internal and external costs of all nodes

        print(f'nodes: {nodes}')

        for node in nodes:
            D[node] = nodes[node][2] - nodes[node][1]  #set D value of component to its external cost minus internal cost

        print(f'D Values: {D}')

        ###############as far as I know, everything UP TO here works correctly######################

        #######everything below is a loop to execute a single iteration of the KL algorithm#########

        g = {}  # dict used to store gains of edges
        gainValues = [0]  # will be used to hold max gain value for the end of each loop of each iteration
        gMax = -999 #will be used to hold max accumulated gain to determine if better partitions are found

        partA = optPartA #each time we iterate, we want to unlock all and use the best found partitions
        partB = optPartB

        print("FINISHED ONE ITERATION, MOVING ON TO THE NEXT ONE")

        for x in range((len(nodes)-1)//2): #here we will loop through all the nodes (need to lock all each iteration)

            g = gain(partA, partB, nodes, modE, D, g)

            maxKey = max(g, key=g.get) #this will find the key (tuple representing edge) pertaining to the max gain value

            swapNodes(nodes, maxKey, partA, partB, D, modE)

            temp0 = list(nodes[maxKey[0]])
            temp0[4] = 1
            nodes[maxKey[0]] = tuple(temp0)
            temp1 = list(nodes[maxKey[1]])
            temp1[4] = 1
            nodes[maxKey[1]] = tuple(temp1)
            gainValues.append(g[maxKey] + gainValues[-1]) #append the max calculated gain to the accumulated gain, after adding it to the most recent value

            if gainValues[-1] > gMax:  # if we have reached a new global maximum for accumulated gain, update the maximum gain and optimal partition
                gMax = gainValues[-1]
                optPartA = partA
                optPartB = partB

        for node in nodes: #here we will unlock all values before continuing to the next iteration
            temp = list(nodes[node])
            temp[4] = 0
            nodes[node] = tuple(temp)

        for node in optPartA: #here we will reset our partition indicators to the optimal partitions found
            temp = list(nodes[node])
            temp[3] = "a"
            nodes[node] = tuple(temp)

        for node in optPartB:
            temp = list(nodes[node])
            temp[3] = "b"
            nodes[node] = tuple(temp)

    ieCost(nodes, modE)  #recalculate external cost so we can determine final cut-size

    totExCost = 0 #will be used to keep track of the total external cost of the bi-partitions

    for node in nodes:
        totExCost += nodes[node][2]

    print(f'Final cut-size: {totExCost//2}')
    print(f'Optimal Partition A: {optPartA}')
    print(f'Optimal Partition B: {optPartB}')
    print(f'Edge List: {modE}')