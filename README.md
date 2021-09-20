# KLAlgorithm

This goal of this algorithm is to take 2 files containing a netlist in hypergraph notation and component names/sizes, and optimally partition the set. This is an implementation of the KL algorithm, which is a greedy iterative improvement method.

Inputs:

  -when the main file (hyperMain.py) is ran, the user will be prompted to choose 2 files
  
  -the text files test.txt and test-are.txt are examples of the files that are needed as inputs
  
  -the files need to be chosen test.txt and test-are.txt in that order
  
  -at this point, the algorithm will do all the necessary computation
  

Notation:

  -nodes is a dict, holding values with the following notation: {'nodeName': ('nodeSize',internalCost,externalCost,parition,lockValue)}
  
  -modE is a dict, holding values with the following notation: {('node1',node2'): modifiedEdgeWeight}
  
  -partA and partB are the partitions produced by the algorithm, and will be variable length lists (though will be constrained to nxn where 2n is the number of nodes 
