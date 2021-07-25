import numpy as np

class Ideology:

    def __init__(self, no_agent, no_party):
        self.ideology_low = 1
        self.ideology_high = 100
        self.no_agent = no_agent
        self.no_party = no_party

    def assign_agent_ideology(self, agent):
        agent_ideology_distribution = np.random.randint(self.ideology_low, self.ideology_high, self.no_agent)

        for i in range(0, self.no_agent):
            agent[i].ideology = agent_ideology_distribution[i]

        return agent

    def assign_party_ideology(self, party):
        party_ideology_distribution = np.random.randint(self.ideology_low, self.ideology_high, self.no_party)

        for i in range(0, self.no_party):
            party[i].ideology = party_ideology_distribution[i]

        return party