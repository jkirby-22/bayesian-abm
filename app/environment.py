from node import Node
import numpy as np
class Environment:
    def __init__(self, parameters):
        self.network = [] #Network is node list but with correct shape
        self.node = []
        self.parameters = parameters
        self.x = None
        self.y = None

    def build_network(self, agent): #Could make more modular?
        id = 0
        for x in range(0, 13):
            self.network.append([])
            for y in range(0, 13):
                node = Node(id=id, x=x, y=y, agent_id=agent[id].id)
                self.network[x].append(node)
                self.node.append(node)
                id += 1
        np.reshape(self.network, (13, 13))
        self.x = 13 #Not modular at all!
        self.y = 13

    def get_node(self, agent_id):
        return self.node[agent_id]

    def get_neighbour_ids(self, agent_id): #not most effecient but more modular, discuss or review
        nodes = self.get_neighbour_nodes(agent_id=agent_id, level=self.parameters['level'])
        agents = []
        for node in nodes:
            agents.append(node.agent_id)
        return agents

    def get_neighbour_nodes(self, agent_id, level): #this function could deffo be cleaner
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

    def print_network(self):
        for node in self.node:
            print('Node: ' + str(node.id) + 'Agent ID: ' + str(node.agent_id) + ' x: ' + str(node.x) + ' y: ' + str(node.y))



