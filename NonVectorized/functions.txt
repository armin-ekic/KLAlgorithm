"""This file will be used to define all the necessary functions of the algorithm"""

from tkinter import Tk

from tkinter.filedialog import askopenfilename, askopenfilenames


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
    while True: #loop through the .are file to obtain all components and their sizes
        compLine = compSizes.readline()
        if not compLine:
            break
        nodes[compLine[:2]] = (compLine[len(compLine)-2], float(0), float(0)) #tuple with key as component
        #value of dict is tuple with component size, internal cost, and external cost (initially 0)

    #here we will iterate through the file and interpret the netlist for our hyperedges
    while True:
        netLine = netList.readline() #read the next line of the file
        if count >= 5:
            if not netLine:
                E.append(tuple(hyperEdge))
                break
            if "s" in netLine:
                if hyperEdge:
                    E.append(tuple(hyperEdge))
                hyperEdge = [netLine[len(netLine)-2], netLine[:2]]
            else:
                hyperEdge.append(netLine[:2])
        count+=1

    modE = netCut(E)
    print(f'nodes: {nodes}')
    print(f'E: {E}')
    print(f'modeE: {modE}')
    return nodes, E, modE


# this function will take the partitions and determine internal/external costs of each component
# arguments:
#   P1 and P2 are lists containing the components in each partition
#   nodes is the component dictionary, keys are components, values are tuples of component size, internal cost, and
#       external cost (in that order)
#   modE is the modified edge dictionary containing edge pairs as keys and their weights as values
def ieCost(P1, P2, nodes, modE):
    for edge in modE:
        temp0 = list(nodes[edge[0]]) #temporary variable used to manipulate the internal cost
        temp1 = list(nodes[edge[1]]) #temporary variable used to manipulate the external cost
        if edge[0] in P1 and edge[1] in P2: #if they are in opposite partitions
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
