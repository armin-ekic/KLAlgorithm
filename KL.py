"""This file will run the KL algorithm and return the best partition"""

from functions import *


def main():

    #nodes is the set of vertices (components) from the netlist
    #E is the hyperedge set with corresponding weights for each net
    #modE is the graphical representation of the hyperedge set
    nodes, E, modE = hyperGraph() #this will call the function and obtain desired KL inputs

    #partA and partB are the bi-partitions for the algorithm
    partA = list(nodes.keys())[:len(nodes)//2]
    partB = list(nodes.keys())[len(nodes)//2:]

    optPartA = partA #holds the optimal partition A, initializes to partA
    optPartB = partB #holds the optimal parition B, initializes to partB

    D = {} #dict used to store D values of components

    for i in range(4): #here we are doing 5 total iterations

        ieCost(partA, partB, nodes, modE) #determine internal and external costs of all nodes

        ###############as far as I know, everything UP TO here works correctly######################

        #######everything below is a loop to execute a single iteration of the KL algorithm#########


        locked = [] #list used to store currently locked components      #I'm hoping that re-initializing them like this will essentially clear their values and let me reuse them from an empty state
        g = {}  # dict used to store gains of edges
        gainValues = [0]  # will be used to hold max gain value for the end of each loop of each iteration
        gMax = -999 #will be used to hold max accumulated gain to determine if better partitions are found

        partA = optPartA #each time we iterate, we want to unlock all and use the best found partitions
        partB = optPartB

        for x in range((len(nodes)-1)//2): #here we will loop through all the nodes (need to lock all each iteration)

            for x in nodes:  # here we loop through the nodes dict to calculate our D values for unlocked nodes
                if nodes[x] not in locked:
                    D[x] = nodes[x][2] - nodes[x][1]  # set D value of component to its external cost minus internal cost

            for edge in modE: #this loop will go through the edge pairs and calculate gain values
                if edge[0] not in locked and edge [1] not in locked: #we are only concerned with gains for non-locked values
                    g[edge] = D[edge[0]] + D[edge[1]] - 2*(modE[edge]) #gxy = Dx + Dy - 2Cxy

            maxKey = max(g, key=g.get) #this will find the key pertaining to the max gain value

            if maxKey[0] in partA: #here we will swap the nodes if the first node in the edge is in partition A
                nodeAIndex = partA.index(maxKey[0])
                nodeBIndex = partB.index(maxKey[1])
                nodeA = partA[nodeAIndex]
                partA[nodeAIndex] = partB[nodeBIndex]
                partB[nodeBIndex] = nodeA

            else: #here we will swap the nodes if the first node in the edge is in partition B
                nodeAIndex = partA.index(maxKey[1])
                nodeBIndex = partB.index(maxKey[0])
                nodeA = partA[nodeAIndex]
                partA[nodeAIndex] = partB[nodeBIndex]
                partB[nodeBIndex] = nodeA

            locked.append(maxKey[0])
            locked.append(maxKey[1])
            gainValues.append(g[maxKey] + gainValues[-1]) #append the max calculated gain to the accumulated gain, after adding it to the most recent value

            print(gainValues)

            if gainValues[-1] > gMax: #if we have reached a new global maximum for accumulated gain, update the maximum gain and optimal partition
                gMax = gainValues[-1]
                optPartA = partA
                optPartB = partB