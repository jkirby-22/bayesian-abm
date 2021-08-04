from node import Node
import numpy as np
class Environment:
    def __init__(self, parameters):
        self.network = [] #Network is node list but with correct shape
        self.node = []
        self.parameters = parameters
        self.x = None
        self.y = None

    def build_network(self, agent): #Build the spatial model
        id = 0
        for x in range(0, 13): #number of agents is fixed so harcoded network shape is fine.
            self.network.append([])
            for y in range(0, 13):
                node = Node(id=id, x=x, y=y, agent_id=id) #Associate each agent with a co-ordinate.
                self.network[x].append(node)
                self.node.append(node)
                id += 1
        np.reshape(self.network, (13, 13))
        self.x = 13
        self.y = 13

    def get_node(self, agent_id):
        return self.node[agent_id]

    def get_neighbour_ids(self, agent_id):
        nodes = self.get_neighbour_nodes(agent_id=agent_id, level=self.parameters['level'])
        agents = []
        for node in nodes:
            agents.append(node.agent_id)
        return agents

    def get_neighbour_nodes(self, agent_id, level):
        node = self.get_node(agent_id=agent_id)
        node_list = [node]
        explored_nodes = []
        for i in range(0, level):
            level_nodes = node_list
            for current_node in list(set(node_list).difference(explored_nodes)): #for all unexplored nodes
                level_nodes = list(set(level_nodes + self.get_neighbours(node=current_node)).difference(set(node_list))) #get all neighbours that arent already visited
                explored_nodes.append(current_node) #maybe shouldnt mess with this as its in the loop condition?
            node_list = list(set(node_list + level_nodes))
        return list(set(node_list).difference(set([node]))) #remove own agent

    def get_neighbours(self, node):
        if node.x + 1 > self.x - 1:
            x_plus = 0
        else:
            x_plus = node.x + 1

        if node.x - 1 < 0:
            x_minus = self.x - 1

        else:
            x_minus = node.x - 1

        if node.y + 1 > self.y - 1:
            y_plus = 0
        else:
            y_plus = node.y + 1

        if node.y - 1 < 0:
            y_minus = self.y - 1
        else:
            y_minus = node.y - 1
        return [self.network[x_plus][node.y], self.network[node.x][y_minus], self.network[x_minus][node.y], self.network[node.x][y_plus],
                self.network[x_plus][y_plus], self.network[x_plus][y_minus], self.network[x_minus][y_minus], self.network[x_minus][y_plus]]




