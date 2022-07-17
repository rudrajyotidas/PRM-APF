import numpy as np
import matplotlib.pyplot as plt

def makePoly(vertexList, fillColor = 'red'):

    '''
    vertexList: List of vertices of the polygon you want to draw, 
                as an nx2 numpy array

    fillColor: Colour of the polygon as a string
    '''

    plt.scatter(vertexList[:, 0], vertexList[:, 1], s=0.1, color=fillColor)
    p = plt.Polygon(vertexList, color=fillColor)
    plt.gca().add_patch(p)

def markNodes(nodeXYList, nodeColor='blue'):

    '''
    nodeXYList: List of nodes, as an nx2 numpy array
    nodeColor: Color of nodes as a string
    '''

    plt.scatter(nodeXYList[:,0], nodeXYList[:,1], s=50, color=nodeColor)

def drawEdge(node_1, node_2, Edgecolor='green'):

    '''
    node_1 and node_2: The nodes you want to join with an edge
    Edgecolor: Color of the edge
    '''

    x_arr = np.array([node_1[0], node_2[0]])
    y_arr = np.array([node_1[1], node_2[1]])
    plt.plot(x_arr, y_arr, linewidth=3, color = Edgecolor)