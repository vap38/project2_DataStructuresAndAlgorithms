#
# Created by: Yevhenii Ganusich
# IMPORTANT NOTE: Please run this script using python Graph.py and NOT python3 Graph.py to avoid any compilation errors.
# The tests for all the functions are in Main
#

import random
import sys


# Class for Graph node object
class GraphNode:
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val
        self.neighbors = list()
        self.parent = None


# Class for Graph object
class GridGraph:
    def __init__(self):
        self.cells = list()

    # This function adds grid node to the grid
    def addGridNode(self, x, y, nodeVal):
        newNode = GraphNode(x, y, nodeVal)
        self.cells.append(newNode)

    # This function adds undirected edge between first and second node
    def addUndirectedEdge(self, first, second):
        # Boolean to check whether they could be neighbors
        realNeighbors = False
        if first.x + 1 == second.x and first.y == second.y or first.x - 1 == second.x and first.y == second.y:
            realNeighbors = True
        if first.x == second.x and first.y + 1 == second.y or first.x == second.x and first.y - 1 == second.y:
            realNeighbors = True
        # If they are neighbors
        if realNeighbors:
            # Retrieve the indexes of both nodes within the list
            index1 = -1
            index2 = -1
            # Look them up in the list
            for node in self.cells:
                if node.x == first.x and node.y == first.y:
                    index1 = self.cells.index(node)
                if node.x == second.x and node.y == second.y:
                    index2 = self.cells.index(node)
            # If both nodes are in the graph
            if index1 != -1 and index2 != -1:
                self.cells[index1].neighbors.append(self.cells[index2])
                self.cells[index2].neighbors.append(self.cells[index1])

    # This function removes undirected edge between first and second node
    def removeUndirectedEdge(self, first, second):
        # Retrieve the indexes of both nodes within the list
        index1 = -1
        index2 = -1
        # Look them up in the list
        for node in self.cells:
            if node.x == first.x and node.y == first.y:
                index1 = self.cells.index(node)
            if node.x == second.x and node.y == second.y:
                index2 = self.cells.index(node)
        # If both nodes are in the graph
        if index1 != -1 and index2 != -1:
            self.cells[index1].neighbors.remove(self.cells[index2])
            self.cells[index2].neighbors.remove(self.cells[index1])

    # This function returns all the cells that exist in the graph
    def getAllNodes(self):
        return self.cells


# This function creates (n*n) random nodes and with random, unweighted bidirectional edges
def createRandomGridGraph(n):
    newGraph = GridGraph()
    counter = 0
    # Populate the grid (each cell value stores its sequential position in the grid)
    for y in range(n):
        for x in range(n):
            newGraph.addGridNode(x, y, counter)
            counter += 1
    # Iterate over each cell in the graph
    for cell in newGraph.cells:
        # A list storing all possible neighbors
        possibleNeighbors = []
        # Check for all possible neighbors and add them to the list
        possibleNeighbor1 = cell.val-1
        # If possibleNeighbor1 is within the grid
        if 0 <= possibleNeighbor1 < n * n:
            # If both cells are on the same y level
            if cell.y == newGraph.cells[possibleNeighbor1].y:
                possibleNeighbors.append(possibleNeighbor1)
        possibleNeighbor2 = cell.val+1
        # If possibleNeighbor2 is within the grid
        if 0 <= possibleNeighbor2 < n * n:
            if cell.y == newGraph.cells[possibleNeighbor2].y:
                possibleNeighbors.append(possibleNeighbor2)
        possibleNeighbor3 = cell.val+n
        # If possibleNeighbor3 is within the grid
        if 0 <= possibleNeighbor3 < n * n:
            if cell.x == newGraph.cells[possibleNeighbor3].x:
                possibleNeighbors.append(possibleNeighbor3)
        possibleNeighbor4 = cell.val-n
        # If possibleNeighbor4 is within the grid
        if 0 <= possibleNeighbor4 < n * n:
            if cell.x == newGraph.cells[possibleNeighbor4].x:
                possibleNeighbors.append(possibleNeighbor4)
        # Iterate through every possible neighbor
        for possNeighbor in possibleNeighbors:
            # Make sure the connection doesn't exist yet
            if newGraph.cells[possNeighbor] not in cell.neighbors and cell not in newGraph.cells[possNeighbor].neighbors:
                # Each possible neighbor can have 50% chance of connecting with the current node
                possibility = random.randint(0, 1)
                # If possibility is 1, create connection between the nodes, otherwise do nothing
                if possibility > 0:
                    cell.neighbors.append(newGraph.cells[possNeighbor])
                    newGraph.cells[possNeighbor].neighbors.append(cell)
    return newGraph


# Helper function which takes in distances dictionary and visited set, returns node with smallest distance
def minDist(distances, visited):
    ans = None
    m = sys.maxint
    for curr in distances.keys():
        if curr not in visited and distances[curr] <= m:
            m = distances[curr]
            ans = curr
    return ans


# Helper function to calculate heuristics in the A* algorithm
def heuristics(curr, dest):
    return abs(dest.x - curr.x) + abs(dest.y - curr.y)


# Returns A* path from sourceNode to destNode
def astar(sourceNode, destNode):
    # Instantiate distances dictionary
    distances = {}
    # Set the distance for the origin to 0.
    distances[sourceNode] = 0
    # Best path
    bestPath = []
    # Visited set
    visited = set()
    # Set curr equal to start
    curr = sourceNode

    # While curr is not empty and not equal to maxint
    while curr is not None:
        # If we found the destination node, traverse back through its parents and append every node in front of list
        if curr == destNode:
            bestPath.insert(0, curr)
            parent = curr.parent
            while parent:
                bestPath.insert(0, parent)
                # Get the parent of the current parent
                parent = parent.parent
            break
        # Finalize curr
        visited.add(curr)
        # Iterate over its neighbors
        for neighbor in curr.neighbors:
            # If the neighbor is not in the distances dictionary yet or the new shorter distance is found
            if neighbor not in distances or distances[neighbor] > distances[curr] + 1 + heuristics(neighbor, destNode):
                # Update the distances
                distances[neighbor] = distances[curr] + 1 + heuristics(neighbor, destNode)
                # Update the parent node
                neighbor.parent = curr
        # Look for next node that is unvisited and has the smallest distance
        curr = minDist(distances, visited)

    return bestPath


if __name__ == "__main__":
    # Create 100 x 100 graph with 9999 cells
    graph = createRandomGridGraph(100)
    # Print the graph
    for i in graph.cells:
        print("X:" + str(i.x) + " Y:" + str(i.y) + " => Value: " + str(i.val))
    # Begin traversal using AStar
    print("Running AStar on grid with " + str(len(graph.cells)) + " cells...")
    list1 = astar(graph.cells[0], graph.cells[9999])
    print("AStar path from 0 to 9999: ")
    if len(list1) == 0:
        print("Path not found")
    else:
        print(" => ".join("[X:" + str(every.x) + " Y:" + str(every.y) + "]" for every in list1))