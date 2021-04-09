from node import Node
import numpy as np
class Environment:
    def __init__(self, x, y, agent):
        self.network = [] #np.empty((x, y))
        #print(self.network.shape)
        self.node = []
        self.x = x
        self.y = y
        id = 0
        for i in range(0, x):
            self.network.append([])
            for z in range(0, y):
                node = Node(id=id, x=i, y=z, agent_id=agent[id].id)
                self.network[i].append(node)
                self.node.append(node)
                id += 1
        np.reshape(self.network, (x, y))

    def get_node(self, agent_id):
        return self.node[agent_id]

    def get_neighbour_agents(self, agent_id):
        node = self.get_node(agent_id=agent_id)
        return self.get_neighbour_nodes(node=node)

    def get_neighbour_nodes(self, node):
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


