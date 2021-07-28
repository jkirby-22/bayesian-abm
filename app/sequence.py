from agent import Agent
from party import Party
from ideology import Ideology
from environment import Environment
from parameters import Parameters
from results import Results
import cProfile
import sys

class Sequence:

    def __init__(self, mode): #Maybe make ideology modular so it could be multi dimminesional

        self.parameters = Parameters(mode=int(mode)).get_parameters()
        self.ideology = Ideology(no_agent=self.parameters['no_agent'], no_party=self.parameters['no_party']) #discuss how you wanna keep all data access in same variablres to avoid potential inconsistencies

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

    def get_vote_share(self):
        votes = [0, 0, 0]
        for voter in self.agent:
            votes[voter.previous_vote_id] = votes[voter.previous_vote_id] + 1
        distribution = [round(vote / len(self.agent), 2) for vote in votes]
        return distribution

    #Creation procedures
    def create_agents(self):
        agent = []
        for id in range(0, self.parameters['no_agent']):
            agent.append(Agent(id=id, parameters=self.parameters))
        self.agent = self.ideology.assign_agent_ideology(agent)
        self.create_environment(agent)

    def create_environment(self, agent):
        self.environment = Environment(parameters=self.parameters)
        self.environment.build_network(agent=agent)

    def create_parties(self):
        party = []
        for id in range(0, self.parameters['no_party']):
            party.append(Party(id=id, parameters=self.parameters))
        self.party = self.ideology.assign_party_ideology(party)

    #Election procedures
    def inital_election(self):
        for agent in self.agent:
            agent.pure_vote(parties=self.party)
        print('initial election: ')
        print(self.get_vote_share())


    def election(self):
        for agent in self.agent:
            neighbours = []
            for id in self.environment.get_neighbour_ids(agent_id=agent.id):
                neighbours.append(self.agent[id])
            agent.choose_vote(parties=self.party, neighbours=neighbours) #TRADE OFF HERE 1!!!! INN THE LOOP ABOVE!!
        for agent in self.agent: #Have to submit it after choice to prevent update or previous vote id
            agent.submit_vote()

    #run procedures
    def round(self):
        #Create agents, parties and perform initial election.
        sim.create_agents()
        sim.create_parties()
        self.inital_election()

        #perform elections
        for i in range(0, self.parameters['elections']):
            self.election()

    def run(self):
        run_id = self.results.insert_run(parameters=self.parameters)
        for i in range(0, self.parameters['rounds']):
            #Run round of elections
            self.round()
            objects = [self.agent, self.party, self.environment, self.parameters] #pass all key objects to results for analysis
            self.results.insert_round(objects=objects, run_id=run_id)

            #reset key components
            self.party = []
            self.agent = []
            self.environment = None
        return run_id

    #Keep tests for class in file using main (ref: https://stackoverflow.com/questions/22492162/understanding-the-main-method-of-python)

if __name__ == '__main__':
    sim = Sequence(mode=sys.argv[1])
    cProfile.run('sim.run()')
    #sim.results.print_results(run_id)




