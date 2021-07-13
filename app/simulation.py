import numpy as np #put numpy in one file
from agent import Agent
from party import Party
from environment import Environment
from results import Results
import sys
from barycentric_system import BarycentricSystem

class Simulation: #Do we need a class for this?

    def __init__(self, ideology_low, ideology_high, no_party): #Maybe make ideology modular so it could be multi dimminesional
        self.ideology_low = ideology_low
        self.ideology_high = ideology_high
        self.no_agent = 169
        self.no_party = no_party
        #self.agent = []
        self.party = [] #store in environment
        self.environment = None
        self.results = Results()
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
        agent = []
        for ideology in agent_ideology_distribution:
            agent.append(Agent(id=id, ideology=ideology))
            id += 1
        #np.reshape(self.agent, (13, 13))
        self.create_environment(agent)

    def create_environment(self, agent):
        self.environment = Environment(x=13, y=13, agent=agent) #make specific to number of agents

    def create_parties(self): #Maybe put this in environment?
        party_ideology_distribution = np.random.randint(self.ideology_low, self.ideology_high, self.no_party)
        id = 0
        for ideology in party_ideology_distribution:
            self.party.append(Party(id=id, ideology=ideology))
            id += 1

    def get_vote_count(self):
        agents = sim.environment.get_agent(id=None)
        votes = [0, 0, 0]  # change more modular
        for agent in agents:
            votes[agent.previous_vote_id] = votes[agent.previous_vote_id] + 1
        return votes

    def get_vote_share(self):
        agents = sim.environment.get_agent(id=None)
        votes = [0, 0, 0]  # change more modular
        for agent in agents:
            votes[agent.previous_vote_id] = votes[agent.previous_vote_id] + 1

        distribution = [round(vote / len(agents), 2) for vote in votes]
        return distribution

    def inital_election(self):
        agents = sim.environment.get_agent(id=None)
        for agent in agents:
            elected = agent.pure_vote(self.party)


    def election(self, level):
        agents = self.environment.get_agent(id=None)
        for agent in agents:
            agent.choose_vote(parties=self.party, environment=self.environment, level=level) #maybe return vote here aswell so no second loop needed?
        for agent in agents: #Have to submit it after choice to prevent update or previous vote id
            agent.submit_vote()

    def round(self, no_elections, level):
        sim.create_agents()
        sim.create_parties()
        self.inital_election()
        print('Initial Election: ' + str(self.get_vote_share()))

        for i in range(0, no_elections):
            self.election(level)

        results = { #not extensible will have to change this code if you want different results
            "vote_count": self.get_vote_count(),
            "vote_share": self.get_vote_share() #don't need vote share and count as can be deducted
        }

        # garbage colleciton needed or auto?
        self.party = []
        self.environment = None
        return results

    def run(self, no_elections, level, rounds):
        row = {
            "level": level,
            "no_of_agents": self.no_agent,
            "no_of_parties": self.no_party
        }
        run_id = self.results.insert_run(row=row)
        for i in range(0, rounds):
            self.results.insert_round(row=self.round(no_elections=no_elections, level=level), run_id=run_id)
            print('round: ' + str(i) + ' Complete.')
        return run_id
    #Keep tests for class in file using main (ref: https://stackoverflow.com/questions/22492162/understanding-the-main-method-of-python)

if __name__ == '__main__':
    sim = Simulation(ideology_low=1, ideology_high=100, no_party=3)
    print('Level: ' + str(sys.argv[1]))
    print('Final Election: ' + str(sim.round(20, int(sys.argv[1]))['vote_share']))


