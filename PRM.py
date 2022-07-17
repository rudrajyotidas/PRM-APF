import numpy as np
import random
from sklearn.neighbors import KDTree

class Polygon:

    def __init__(self, pointlist:list):

        self.vertices = []
        self.N = int(len(pointlist)/2)

        for i in range(0, len(pointlist), 2):
            self.vertices.append((pointlist[i], pointlist[i+1]))

    def isfree(self, point:tuple)->bool:

        i=0
        j=self.N-1
        inside = False

        x = point[0]
        y = point[1]

        while(i<self.N):

            xV1, yV1 = self.vertices[i]
            xV2, yV2 = self.vertices[j]

            if (((yV1 <= y) and (y < yV2)) or ((yV2 <= y) and (y < yV1))) and (x < (xV2 - xV1)*(y - yV1)/(yV2 - yV1) + xV1):
                inside = not inside

            j = i
            i = i+1
        
        return not inside

class Map:

    def __init__(self, xlim:int, ylim:int, obstaclesFilename='obstacles.txt'):
        self.xlim = xlim
        self.ylim = ylim

        self.obstacles = []

        file = open(obstaclesFilename, 'r')
        Lines = file.readlines()

        for line in Lines:
            vertices = []
            str = line.split()

            for i in str:
                vertices.append(int(i))

            self.obstacles.append(Polygon(vertices))
    

class PRM:

    def __init__(self, map:Map, N:int, k:int):

        self.N = N
        self.k = k

        self.nodes = np.empty(shape=[0,2])
        self.rejected_nodes = np.empty(shape=[0,2])
        self.graph = np.empty(shape=[N,0])
        self.augmentedGraph = np.empty(shape=[N+2,0])

    def sampleNodes(self)->np.ndarray:

        xlim = map.xlim
        ylim = map.ylim

        count = 0

        while count<self.N:

            node_x = random.uniform(0,xlim)
            node_y = random.uniform(0,ylim)

            free = True

            for obstacle in map.obstacles:

                if obstacle.isfree((node_x, node_y)):
                    free = True
                else:
                    free = False
                    break

            if free:
                self.nodes.append(np.array([node_x, node_y]))
                count = count + 1
            else:
                self.rejected_nodes.append(np.array([node_x, node_y]))

    def buildGraph(self, k=3):

        self.kdt = KDTree(self.nodes)
        nn = self.kdt.query(self.nodes, k)

        for lists in nn:
            self.graph.append(lists)

    def augmentGraph(self, source:list, goal:list, k=3):

        q = np.row_stack(source, goal)
        nn = self.kdt.query(q)

        for lists in self.graph:
            self.augmentedGraph.append(lists)

        self.augmentedGraph.append(nn[0])
        self.augmentedGraph.append(nn[1])
