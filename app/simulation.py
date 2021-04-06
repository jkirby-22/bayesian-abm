import numpy as np #put numpy in one file
from agent import Agent
from party import Party
from environment import Environment
class Simulation: #Do we need a class for this?

    def __init__(self, ideology_low, ideology_high, no_party): #Maybe make ideology modular so it could be multi dimminesional
        self.ideology_low = ideology_low
        self.ideology_high = ideology_high
        self.no_agent = 169
        self.no_party = no_party
        self.agent = []
        self.party = []
        self.environment = None
        #self.environment = Environment(x=13, y=13) #make this consistent with number of agents

    def print_agents(self):
        for agent in self.agent:
            print('Agent: ' + str(agent.id) + ' Ideology Value: ' + str(agent.ideology))

    def print_parties(self):
        for party in self.party:
            print('Party: ' + str(party.id) + ' Ideology Value: ' + str(party.ideology))

    def create_agents(self): #do we need self?
        #Do we need to take a full sample or take 1 sample per agent?
        agent_ideology_distribution = np.random.randint(self.ideology_low, self.ideology_high, self.no_agent) #is this the right dist?, use =parameters

        id = 0
        for ideology in agent_ideology_distribution:
            self.agent.append(Agent(id=id, ideology=ideology))
            id += 1
        #np.reshape(self.agent, (13, 13))
        self.create_environment()

    def create_environment(self):
        self.environment = Environment(x=13, y=13, agent=self.agent) #make specific to number of agents

    def create_parties(self): #do we need self?
        #Do we need to take a full sample or take 1 sample per agent?
        party_ideology_distribution = np.random.randint(self.ideology_low, self.ideology_high, self.no_party)
        id = 0
        for ideology in party_ideology_distribution:
            self.party.append(Party(id=id, ideology=ideology))
            id += 1

    def election(self):
        for agent in self.agent:
            elected = agent.vote(self.party)
            print('Agent: ' + str(agent.id) + ' Ideology Value: ' + str(agent.ideology))
            print('Voted for: ')
            print('Party: ' + str(elected.id) + ' Ideology Value: ' + str(elected.ideology))


    #Keep tests for class in file using main (ref: https://stackoverflow.com/questions/22492162/understanding-the-main-method-of-python)
if __name__ == '__main__':
    sim = Simulation(ideology_low=1, ideology_high=100, no_party=2)
    sim.create_agents()
    #sim.create_parties()
    sim.environment.print_network()
    neighbours = sim.environment.get_neighbour_agents(agent_id=0)
    node = sim.environment.get_node(agent_id=0)
    print('Agent 0s node: x: ' + str(node.x) + ' y: ' + str(node.y))
    for node in neighbours:
        print('Node: ' + str(node.id) + ' x: ' + str(node.x) + ' y: ' + str(node.y))
    #sim.election()