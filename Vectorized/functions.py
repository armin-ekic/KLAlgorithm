"""This file will be used to define all the necessary functions of the algorithm"""

from __future__ import absolute_import

from tkinter import Tk

from tkinter.filedialog import askopenfilename, askopenfilenames

import numpy

import copy


#this function will convert the hyperedge list into a graphical representation of edges with weights
#arguments:
#   hyperEdgeList is the list of all hyperedges and their corresponding weights in a tuple
#return:
#   modEdge is the modified edge and scaled weight list in graphical representation
#       each modEdge entry is a key value pair in which the key is the edge, and the value is the modified weight
def netCut(hyperEdgeList):

    edges = {}
    for hyperEdge in hyperEdgeList:
        cellCount = len(hyperEdge) - 1 #determine how many cells are present in a given net
        hyperEdgeWeight = float(hyperEdge[0]) #extract the weight of the given net
        modWeight =  1/(cellCount - 1) #determine the scalar applied to the weight
        for x in range(1, len(hyperEdge) - 1):
            for y in range(x +1 , len(hyperEdge)):
                if (hyperEdge[x], hyperEdge[y]) in edges.keys():
                    edges[(hyperEdge[x], hyperEdge[y])] += hyperEdgeWeight*modWeight #if the edge is already listed, add to the existing weight (the same edges won't be counted twice)
                else:
                    edges[(hyperEdge[x], hyperEdge[y])] = hyperEdgeWeight*modWeight

    return edges


#this function will take the hyperedge list and create a lower triangular matrix to house connections and weights
#inputs:
#   nodes is the component dictionary, keys are components, values are tuples of component size, internal cost,
#       external cost (in that order), and an indicator of which partition they are in
#   modE is the modified edge dictionary containing edge pairs as keys and their weights as values
def edgeMatrix(nodes, modE):
    lowerEdgeMatrix = numpy.zeros((len(nodes),len(nodes))) #create an NxN matrix, where N is the number of components
    for x, node1 in enumerate(nodes): #enumerate through the nodes and keep track of indices for the matrix
        for y, node2 in enumerate(nodes):
            if x > y:
                continue
            try:
                lowerEdgeMatrix[y,x] = modE[(node1,node2)]
            except KeyError:
                try:
                    lowerEdgeMatrix[y,x] = modE[(node2,node1)]
                except KeyError:
                    continue
    return lowerEdgeMatrix


#this function will grab the netlist file and convert the data into a set of vertices, hyperedges, and edges
#return:
#   V is the set of components, E is the hyperedge representation of nets, edges is the graphical representation of nets
def hyperGraph():

    #here we will ask the user to choose a file, and open it for reading
    Tk().withdraw() #prevents the root window from appearing
    fileNames = askopenfilenames(title="Select the netlist file first, and the .are file second") #shows "open" dialog box and returns path of desired file
    netList = open(fileNames[0], 'r') #opens the file chosen by the user for reading
    compSizes = open(fileNames[1], 'r')

    E = [] #this will be our set of hyperedges in the hypergraph
    hyperEdge = []
    count = 0

    nodes = {}
    count = 0
    while True: #loop through the .are file to obtain all components and their sizes
        compLine = compSizes.readline()
        compInfo = compLine.split() #split up the information in the line and store in an array
        if not compLine:
            break
        nodes[compInfo[0]] = (compInfo[1], float(0), float(0), "a",  0, count) #tuple with key as component name
        count+=1 #count will be used to keep track of what index can be used to access that node in the lower triangular matrix
        #value of dict is tuple with component size, internal cost, external cost (initially 0), partition that it
        #   is in (initialized to a for all), and locked value (0 for unlocked, 1 for locked)

    #here we will iterate through the file and interpret the netlist for our hyperedges
    count = 0
    while True:
        netLine = netList.readline() #read the next line of the file
        if count >= 5:
            if not netLine:
                E.append(tuple(hyperEdge))
                break
            netInfo = netLine.split() #holds the information for the portion of the net
            if "s" in netLine:
                if hyperEdge:
                    E.append(tuple(hyperEdge))
                hyperEdge = [netInfo[-1], netInfo[0]]
            else:
                hyperEdge.append(netInfo[0])
        count+=1

    modE = netCut(E)
    #print(f'nodes: {nodes}')
    #print(f'E: {E}')
    #print(f'modeE: {modE}')
    return nodes, E, modE


# this function will take the partitions and determine internal/external costs of each component
# arguments:
#   P1 and P2 are lists containing the components in each partition
#   nodes is the component dictionary, keys are components, values are tuples of component size, internal cost,
#       external cost (in that order), and an indicator of which partition they are in
#   modE is the modified edge dictionary containing edge pairs as keys and their weights as values
def ieCost(nodes, modE):
    for edge in modE:
        temp0 = list(nodes[edge[0]]) #temporary variable used to manipulate the internal cost
        temp1 = list(nodes[edge[1]]) #temporary variable used to manipulate the external cost
        if (nodes[edge[0]][3] == "a") and (nodes[edge[1]][3] in "b"): #if they are in opposite partitions
            #nodes[edge[0]][2] will look into the first entry of the edge tuple, and use this to index into the nodes dictionary
            #   [2] will access the value in the nodes tuple pertaining to external cost
            temp0[2] += modE[edge]  #increment the external cost of the first node
            temp1[2] += modE[edge]  # increment the external cost of the second node
            nodes[edge[0]] = tuple(temp0)
            nodes[edge[1]] = tuple(temp1)
        elif (nodes[edge[0]][3] == "b") and (nodes[edge[1]][3] in "a"): #if they are in opposite partitions
            #nodes[edge[0]][2] will look into the first entry of the edge tuple, and use this to index into the nodes dictionary
            #   [2] will access the value in the nodes tuple pertaining to external cost
            temp0[2] += modE[edge]  #increment the external cost of the first node
            temp1[2] += modE[edge]  # increment the external cost of the second node
            nodes[edge[0]] = tuple(temp0)
            nodes[edge[1]] = tuple(temp1)
        else:
            temp0[1] += modE[edge]  # increment the internal cost of the first node
            temp1[1] += modE[edge]  # increment the internal cost of the second node
            nodes[edge[0]] = tuple(temp0)
            nodes[edge[1]] = tuple(temp1)
        del temp0, temp1


#this function will take two nodes based on the two pertaining to the biggest cost, and swap them, then find D prime values
#inputs:
#   nodes is the component dictionary, keys are components, values are tuples of component size, internal cost,
#       external cost (in that order), and an indicator of which partition they are in
#   maxKey is the pair of nodes that reduce the cut-size by the largest amount when swapped
#   partA is the "A" partition
#   partB is the "B" partition
#   D is the dict holding D values for all nodes
#   lowerEdgeMatrix is the matrix used to hold edge weights between node pairs
#   unlockedA is a list of unlocked nodes in partition A, just input in order to update its values
#   unlockedB is a list of unlocked nodes in partition B, just input in order to update its values
#   unlockedLowerEdge is a deep copy of lowerEdgeMatrix with locked rows deleted, input to update its values
def swapNodes(nodes, maxKey, partA, partB, D, lowerEdgeMatrix):
    if nodes[maxKey[0]][3] == "a":  # here we will swap the nodes if the first node in the edge is in partition A
        nodeAIndex = partA.index(maxKey[0])
        nodeBIndex = partB.index(maxKey[1])
        nodeA = partA[nodeAIndex]
        partA[nodeAIndex] = partB[nodeBIndex]
        partB[nodeBIndex] = nodeA
        temp0 = list(nodes[maxKey[0]])
        temp1 = list(nodes[maxKey[1]])
        temp0[3] = "b"
        temp1[3] = "a"
        nodes[maxKey[0]] = tuple(temp0)
        nodes[maxKey[1]] = tuple(temp1)

        temp0 = list(nodes[maxKey[0]])  # here we are indicating that the swapped nodes are locked
        temp0[4] = 1
        nodes[maxKey[0]] = tuple(temp0)
        temp1 = list(nodes[maxKey[1]])
        temp1[4] = 1
        nodes[maxKey[1]] = tuple(temp1)

        for node in nodes:  # here we loop through the nodes dict to calculate our D values for unlocked nodes
            if nodes[node][4] != 1:  # here we calculate the D values for the first step in the iteration
                if nodes[node][3] == "a":  # if this node is in the A partition, and we already have a preexisting D value
                    Cxd = lowerEdgeMatrix[(nodes[node][5], nodes[maxKey[0]][5])]
                    Cxg = lowerEdgeMatrix[(nodes[node][5], nodes[maxKey[1]][5])]
                    D[node] = D[node] + (2 * Cxd) - (2 * Cxg)
                else:
                    Cxd = lowerEdgeMatrix[(nodes[node][5], nodes[maxKey[1]][5])]
                    Cxg = lowerEdgeMatrix[(nodes[node][5], nodes[maxKey[0]][5])]
                    D[node] = D[node] + (2 * Cxd) - (2 * Cxg)
    else:  # here we will swap the nodes if the first node in the edge is in partition B
        nodeAIndex = partA.index(maxKey[1])
        nodeBIndex = partB.index(maxKey[0])
        nodeA = partA[nodeAIndex]
        partA[nodeAIndex] = partB[nodeBIndex]
        partB[nodeBIndex] = nodeA
        temp0 = list(nodes[maxKey[0]])
        temp1 = list(nodes[maxKey[1]])
        temp0[3] = "a"
        temp1[3] = "b"
        nodes[maxKey[0]] = tuple(temp0)
        nodes[maxKey[1]] = tuple(temp1)

        temp0 = list(nodes[maxKey[0]])  # here we are indicating that the swapped nodes are locked
        temp0[4] = 1
        nodes[maxKey[0]] = tuple(temp0)
        temp1 = list(nodes[maxKey[1]])
        temp1[4] = 1
        nodes[maxKey[1]] = tuple(temp1)

        for node in nodes:  # here we loop through the nodes dict to calculate our D values for unlocked nodes
            if nodes[node][4] != 1:  # here we calculate the D values for the first step in the iteration
                if nodes[node][3] == "a":  # if this node is in the A partition, and we already have a preexisting D value
                    Cxd = lowerEdgeMatrix[(nodes[node][5], nodes[maxKey[1]][5])]
                    Cxg = lowerEdgeMatrix[(nodes[node][5], nodes[maxKey[0]][5])]
                    D[node] = D[node] + (2 * Cxd) - (2 * Cxg)
                else:
                    Cxd = lowerEdgeMatrix[(nodes[node][5], nodes[maxKey[0]][5])]
                    Cxg = lowerEdgeMatrix[(nodes[node][5], nodes[maxKey[1]][5])]
                    D[node] = D[node] + (2 * Cxd) - (2 * Cxg)


#this function will take the partitions and calculate the gains pertaining to all possible component pairs
#inputs:
#   nodes is the component dictionary, keys are components, values are tuples of component size, internal cost,
#       external cost (in that order), and an indicator of which partition they are in
#   g is the gain dict holding each pair of nodes and their corresponding gain
#   partA is the "A" partition
#   partB is the "B" partition
#   D is the dict holding D values for all nodes
#   modE is the modified edge dictionary containing edge pairs as keys and their weights as values
def gain(partA, D, nodes, lowerEdgeMatrix, g):
    print("finding gain matrix")
    DValues = []
    for node in nodes:
        DValues.append(D[node])
    DArray = numpy.array(DValues)
    for nodeA in partA:  # this loop will go through the nodes in partition A so we can iterate through the matrix columns
        if nodes[nodeA][4] != 1:
            rowInfo = lowerEdgeMatrix[nodes[nodeA][5], 0:nodes[nodeA][5]] #grab the nodeA-th row, and the first n columns
            columnInfo = lowerEdgeMatrix[nodes[nodeA][5]:, nodes[nodeA][5]] #grab the nodeA-th row to the end in the nth column
            weightData = numpy.concatenate((rowInfo.T, columnInfo))
            gainValues = D[nodeA] + DArray - (2*weightData)
            g = numpy.vstack([g, gainValues]) #add the weights to the gain matrix as a new row
    return g


#this function will grab the dictionary pertaining to gain values and return the maximum pair
def findMaxGain(g, partA, partB, nodes):
    print("finding max gain")
    maxList = {}
    for nodeB in partB:
        #maxInColumn = [max(i) for i in zip(*g)][nodes[nodeB][5]] #find the max value in the column pertaining to each node in partition B
        #print(maxInColumn)
        column = g[:,nodes[nodeB][5]] #grab each column pertaining to the partition B nodes
        nodeAIndex = numpy.argmax(column)-1 #find the row pertaining to the max value in the column, offset to account for first row of min values
        nodeA = partA[nodeAIndex]
        maxList[(nodeA, nodeB)] = column[nodeAIndex]
    maxKey = max(maxList, key=maxList.get) #grab the key pertaining to the maximum gain value
    return maxKey, maxList