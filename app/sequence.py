from agent import Agent
from party import Party
from environment import Environment
from parameters import Parameters
from results import Results
import matplotlib.pyplot as plt
import sys
class Sequence:

    def __init__(self, mode): #Maybe make ideology modular so it could be multi dimminesional

        self.parameters = Parameters(mode=int(mode)).get_parameters()
        self.party = []
        self.agent = []
        self.environment = None
        self.results = Results()

    #Creation procedures

    def create_agents(self):
        for id in range(0, self.parameters['no_agent']):
            self.agent.append(Agent(id=id, parameters=self.parameters))
        self.create_environment(self.agent)

    def create_environment(self, agent):
        self.environment = Environment(parameters=self.parameters)
        self.environment.build_network(agent=agent)

    def create_parties(self):
        for id in range(0, self.parameters['no_party']):
            self.party.append(Party(id=id, parameters=self.parameters))

    #Election procedures

    def inital_election(self): #vote without interaction influence
        for agent in self.agent:
            agent.pure_vote(parties=self.party)

    def election(self):
        for agent in self.agent:
            neighbours = []
            for id in self.environment.get_neighbour_ids(agent_id=agent.id):
                neighbours.append(self.agent[id])
            agent.choose_vote(parties=self.party, neighbours=neighbours) #pass agent their neighbours to interact with

        for agent in self.agent: #Have to submit vote after so that interaction phase is distinctly seprate from voting phase
            agent.submit_vote()

    #Run procedures

    def round(self):
        #Create agents, parties and perform initial election.
        sim.create_agents()
        sim.create_parties()
        self.inital_election()

        #perform elections
        for i in range(0, self.parameters['no_election']):
            self.election()

    def run(self):
        run_id = self.results.insert_run(parameters=self.parameters)
        for i in range(0, self.parameters['no_round']):
            #Run round of elections
            self.round()
            objects = [self.agent, self.party, self.environment, self.parameters] #pass all key objects to results for analysis
            self.results.insert_round(objects=objects, run_id=run_id)

            #reset key components
            self.party = []
            self.agent = []
            self.environment = None
        return run_id

if __name__ == '__main__':
    sim = Sequence(mode=sys.argv[1])
    sim.run()



