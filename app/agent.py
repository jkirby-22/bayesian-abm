from party import Party
from environment import Environment
from barycentric_system import BarycentricSystem
class Agent:
    def __init__(self, id, ideology):
        self.id = id
        self.ideology = ideology
        self.previous_vote_id = None
        self.barycentric_system = BarycentricSystem() #just for effeciency to not create a new one evverytime
        self.new_vote_id = None

    def get_utility(self, party): #so is utility always a negative number?
        return -1 * ((self.ideology - party.ideology)**2) #check bodmas etc

    def get_prospective_rating(self, party, pivot_probabilities, parties):
        rating = 0
        for p in parties:
            if p.id != party.id:
                #explain this with some requirements of ordering ygm
                if p.id < party.id:
                    key = str(p.id) + str(party.id)
                else:
                    key = str(party.id) + str(p.id)
                rating = rating + (pivot_probabilities[key] * (self.get_utility(party=party) - self.get_utility(party=p))) #put party out of loop to reduce func calls
        return rating

    def get_probability_distribution(self, environment, level, no_of_parties): #cant pass agents list as it shouldnt hav e access to that ygm?
        #votes = [0] * no_of_parties
        votes = [0, 0, 0] #change more modular
        neighbours = environment.get_neighbour_agents(agent_id=self.id, level=level)
        for agent in neighbours:
            votes[agent.previous_vote_id] = votes[agent.previous_vote_id] + 1 #(1 / len(neighbours)) CANT DO THIS FOR SOME REASON EVEN THO MORE EFFECIENT?
        distribution = [round(vote / len(neighbours), 2) for vote in votes]
        return distribution

    def submit_vote(self):
        self.previous_vote_id = self.new_vote_id

    def choose_vote(self, parties, environment, level):
        distribution = self.get_probability_distribution(environment=environment, level=level, no_of_parties=len(parties))
        if self.id == 83:
            print("Agent 83's probability distribution: " + str(distribution))
        if self.id == 1:
            print("Agent 1's probability distribution: " + str(distribution))
        pivot_probabilities = self.barycentric_system.get_pivot_probabilities(point=distribution)
        #if self.id == 83:
            #print('p12: ' + str(pivot_probabilities["01"]))
           # print('p13: ' + str(pivot_probabilities["02"]))
            #print('p23: ' + str(pivot_probabilities["12"]))
        choice = None
        choice_rating = None
        for party in parties:
            prospective_rating = self.get_prospective_rating(party=party, pivot_probabilities=pivot_probabilities, parties=parties)
            if choice is None:
                choice = party
                choice_rating = prospective_rating
            elif prospective_rating > choice_rating:
                choice = party
                choice_rating = prospective_rating
        self.new_vote_id = choice.id
        if self.id == 83:
            print("Agent 83s vote: " + str(self.new_vote_id))
        if self.id == 1:
            print("Agent 1s vote: " + str(self.new_vote_id))

    def pure_vote(self, parties): #PUT UTILITY FUNCTION HERE
        utility = None
        choice = None
        for party in parties:
            current_utility = self.get_utility(party=party)
            if choice is None:
                choice = party
                utility = current_utility
            elif current_utility > utility:
                utility = current_utility
                choice = party
        self.previous_vote_id = choice.id
        #if self.id == 83:
            #print("Agent 83s vote: " + str(self.previous_vote_id))
        return choice
