import numpy as np #put numpy in one file
class Simulation: #Do we need a class for this?

    def __init__(self, ideology_low, ideology_high, no_agent, no_party): #Maybe make ideology modular so it could be multi dimminesional
        self.ideology_low = ideology_low
        self.ideology_high = ideology_high
        self.no_agent = no_agent
        self.no_party = no_party

    def create_agents(self): #do we need self?
        agent_ideology_distribution = np.random.uniform(self.ideology_low, self.ideology_high, self.no_agent)
        party_agent_distribution = np.random.uniform(self.ideology_low, self.ideology_high, self.no_party)
        print(agent_ideology_distribution) #TEST
        print(party_agent_distribution) #TEST
