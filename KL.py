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

    #for i in range(4): #here we are doing 5 total iterations

    ieCost(partA, partB, nodes, modE) #determine internal and external costs of all nodes

    print(f'nodes: {nodes}')
