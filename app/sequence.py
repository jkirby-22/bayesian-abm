from agent import Agent
from party import Party
from ideology import Ideology
from environment import Environment
from parameters import Parameters
from results import Results
import sys

class Sequence:

    def __init__(self, mode): #Maybe make ideology modular so it could be multi dimminesional

        self.parameters = Parameters(mode=mode).get_parameters()
        self.ideology = Ideology(no_agent=self.parameters['no_agent'], no_party=self.parameters['no_agent']) #discuss how you wanna keep all data access in same variablres to avoid potential inconsistencies

        self.party = []
        self.agent = []

        self.environment = None
        self.results = Results()

    #Useful for printing, testing and results
    def print_agents(self):
        for agent in self.agent:
            print('Agent: ' + str(agent.id) + ' Ideology Value: ' + str(agent.ideology))

    def print_parties(self):
        for party in self.party:
            print('Party: ' + str(party.id) + ' Ideology Value: ' + str(party.ideology))

    #Creation procedures
    def create_agents(self):
        agent = []
        for id in range(0, self.no_agent):
            agent.append(Agent(id=id))
        self.agent = self.ideology.assign_agent_ideology(agent)
        self.create_environment(agent)

    def create_environment(self, agent):
        self.environment = Environment(agent=agent) #make specific to number of agents
        self.environment.build_network(agent=agent)

    def create_parties(self): #Maybe put this in environment?
        party = []
        for id in range(0, self.no_agent):
            self.party.append(Party(id=id))
        self.party = self.ideology.assign_party_ideology(party)

    #Election procedures
    def inital_election(self):
        for agent in self.agent:
            elected = agent.pure_vote(self.party)

    def election(self, level):
        for agent in self.agent:
            neighbours = []
            for id in self.environment.get_neighbour_ids(agent_id=agent.id, level=level): #Maybe functionalise?
                neighbours.append(self.agent[id])

            agent.choose_vote(parties=self.party, neighbours=neighbours, level=level) #TRADE OFF HERE 1!!!! INN THE LOOP ABOVE!!
        for agent in self.agent: #Have to submit it after choice to prevent update or previous vote id
            agent.submit_vote()

    #run procedures
    def round(self):
        #Create agents, parties and perform initial election.
        sim.create_agents()
        sim.create_parties()
        self.inital_election()
        #print('Initial Election: ' + str(self.get_vote_share()))

        #perform elections
        for i in range(0, self.parameters['no_election']):
            self.election()
            #print('election no: ' + str(i))

    def run(self):
        run_id = self.results.insert_run(parameters=self.parameters)
        for i in range(0, self.parameters['rounds']):
            self.round()
            objects = [self.agent, self.party, self.environment, self.parameters]
            self.results.insert_round(objects=objects, run_id=run_id)
            self.party = []
            self.agent = []
            self.environment = None
            #print('round: ' + str(i) + ' Complete.')
        return run_id

    #Keep tests for class in file using main (ref: https://stackoverflow.com/questions/22492162/understanding-the-main-method-of-python)

if __name__ == '__main__':
    sim = Sequence(mode=sys.argv[1])
    run_id = sim.run(no_elections=5, level=1, rounds=1)
    sim.results.print_results(run_id)




