# KLAlgorithm

This goal of this algorithm is to take 2 files containing a netlist in hypergraph notation and component names/sizes, and optimally partition the set. This is an implementation of the KL algorithm, which is a greedy iterative improvement method.

Inputs:

  -when the main file (hyperMain.py) is ran, the user will be prompted to choose 2 files
  
  -the text files test.txt and test-are.txt are examples of the files that are needed as inputs
  
  -the files need to be chosen test.txt and test-are.txt in that order
  
  -at this point, the algorithm will do all the necessary computation
  

Notation:

  -nodes is a dict, holding values with the following notation: {'nodeName': ('nodeSize',internalCost,externalCost,parition,lockValue,indexableValue)}
  
  -modE is a dict, holding values with the following notation: {('node1',node2'): modifiedEdgeWeight}
  
  -partA and partB are the partitions produced by the algorithm, and will be variable length lists (though will be constrained to nxn where 2n is the number of nodes 


Various versions of project:

  The NonVectorized file contains my initial implementation of the project, my main goal when writing this was just to produce an algorithm that worked, regardless of runtime.
  
  The Vectorized file contains code that puts some of the data sets (such as the gain values) in matrix form, so as to improve efficiency of the code.
  
  The differences are described in slightly more detail below.


What this project taught me:

  I will preface this by saying that I am still working on improving the code and its efficiency. There are lots of areas that need to be cleaned up, and some comments that could improve documentation.
  
  Coding this algorithm in python gave me a better understanding of how python structures such as tuples and dictionaries work. I might have been more successfull creating objects to represent nodes, edges, etc., but this is an implementation that I chose to stuck with (not to mention I already understand how objects work for the most part). 
  
  I became more aware of memory storage and the effect that a few changes can make to execution speed. The algorithm is meant to handle files containing hundreds of thousands, and potentially millions of nodes, so having loops that take a substantial amount of time to execute slowed down the project significantly. One thing I did to change this is leaning heavily on key-value pairs to keep track of relevant data for all the edges and nodes.
  
  One of the major keys in fixing issues was the debugging tool. This is something that I have neglected in the past and have ignored for the most part. I made use of the debugger to figure out that I was incorrectly calculating the D value, that my gain calculations were incorrect, that my optimal partition lists and current partition lists were being handeled by the same pointer, and much more.
  
  I learned how to better handle resources, and reduce the amount of memory allocated during runtime. As far as improving the execution speed of the project, vectorization and matrix representations of data sets were used to do as many calculations in parallel as possible. While this did not speed up the project as I hoped it would, it drastically reduced the amount of memory used during the algorithm's runtime. Without the matrix representation of the data sets (code shown in NonVectorized folder), the algorithm ate up about 5.1 GB of memory, while the matrix representation of data sets (shown in Vectorized folder) reduced the memory usage to about 2.6 GB. So I can say that while I did not successfully reduce the execution time of the algorithm, I learned how to manage my resources more effectively.
