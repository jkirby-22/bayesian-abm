from party import Party
from environment import Environment
from barycentric_system import BarycentricSystem
class Agent:
    def __init__(self, id, ideology):
        self.id = id
        self.ideology = ideology
        self.previous_vote_id = None
        self.barycentric_system = BarycentricSystem() #just for effeciency to not create a new one evverytime

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
        distribution = [vote / len(neighbours) for vote in votes]
        return distribution

    def vote(self, parties, environment, level):
        distribution = self.get_probability_distribution(environment=environment, level=level, no_of_parties=len(parties))
        pivot_probabilities = self.barycentric_system.get_pivot_probabilities(point=distribution)
        prospective_rating = []
        for party in parties:
            prospective_rating.append(self.get_prospective_rating(party=party, pivot_probabilities=pivot_probabilities, parties=parties))
        #print("Prospective rating: " + str(prospective_rating))
        #print("Pivot probabilities: " + str(pivot_probabilities))

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
        return choice
