"""
Uniform Cost Search

Takes an input of an n x n matrix of integers, representing the distance between nodes on a graph.  Uses uniform cost search to find a path from the node 1 to node n.

Outputs the path to path.txt, and the nodes that were searched in searched.txt.

"""

import sets
import sys
import heapq

#wrapper around heap
class PriorityQ(object):
    def __init__(self):
        self.heap = []
    def get(self):
        return heapq.heappop(self.heap)
    def put(self,priority,node,parent):
        heapq.heappush(self.heap,(priority,node,parent))
    def empty(self):
        return (self.heap == []) 


#reads file for matrix
#requires exact formating, i.e. all comment are lines starting with '#'
#and matrices are n x n, space delimited blocks of integers
def parse_file():
    result_matrix = []
    f = open(sys.argv[1],'r')
    for line in f.readlines():
        if not(line[0] == '#' or line.strip() == ""):
            line = line.split()
            result_matrix.append(map(int,line))
    f.close()
    return result_matrix

def ucs(matrix,root,finish):
    #intialize variables
    root_cost = 0
    marked = sets.Set() #nodes that have been processed
    origins = dict() #keep track of parents to rebuild path
    visited_nodes = [] #nodes added to queue, in order
    upcoming_nodes = PriorityQ() #"frontier"
    
    #base case
    origins[root]=None
    upcoming_nodes.put(root_cost,root,None)

    #iteration
    while(not(upcoming_nodes.empty())):
        """
        Instead of updating priority, we just load up all child nodes that haven't been marked.
        So we only process it the first time, and ignore all future times it shows up.
        Since a node will be processed and added to marked if and only if it is the shortest path from root to the node,
        this is still correct.
        But we're sacrificing memory so we don't have to write a replace function
        
        The rest is standard.  Process the next node on the priority queue:
        If it's the finish node (goal), rebuild the path, and return the path and nodes that have been visited.
        Otherwise, add the children that haven't been processed to the priority queue, with priority = cost from root to child
        """
        cost,node,parent = upcoming_nodes.get()
        if(node not in marked): #ignore previously processed nodes
            origins[node]=parent
            visited_nodes.append(node)
            marked.add(node)

            if (node == finish):
                return rebuild(node,origins),visited_nodes

            node_children = [ index  for index, element in enumerate(matrix[node]) if element!=0 ]
            for child in node_children:           
                if(child not in marked):
                    upcoming_nodes.put(cost + matrix[node][child],child,node)
    return None

#rebuilds path from predecessors
def rebuild(node, origins):
    result = [node]
    current = node
    while(origins[current]!=None):
        current = origins[current]
        result.append(current)
    result.reverse()
    return result
    
def main():
    #parse file
    if len(sys.argv) < 2:
        print "Error: Not enough inputs"
        sys.exit()
    incidence_matrix = parse_file()

    #run algorithm
    path,searched = ucs(incidence_matrix,0,len(incidence_matrix)-1)

    #output to path.txt and searched.txt
    output_path = open("path.txt",'w')
    output_searched = open("searched.txt",'w')
    
    for node in path:
        output_path.write(str(node)+'\n')
    for node in searched:
        output_searched.write(str(node)+'\n')

main()
