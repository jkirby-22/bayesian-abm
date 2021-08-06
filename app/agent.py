import numpy as np
import math
from barycentric_system import BarycentricSystem
class Agent:
    def __init__(self, id, parameters):
        self.id = id
        self.ideology = np.random.randint(1, 100) #sample ideology from a uniform distribution

        self.parameters = parameters

        self.previous_vote_id = None
        self.new_vote_id = None
        self.pure_vote_id = None

        self.barycentric_system = BarycentricSystem()

        self.population = parameters['no_agent'] - 1 #Need to write that it excludes the current agent in model write up
        self.candidates = parameters['no_party'] #needs to be 3 regardless
        self.vote_events = self.stars_and_bars(stars=self.population, bars=self.candidates - 1)
        self.win_events = self.get_win_events()

    #bayesian methods

    def get_win_events(self):
        i = self.population
        count = 0
        while True:
            spare = self.population - i #number of outcomes for a given i
            if i > spare:
                count = count + self.stars_and_bars(stars=spare, bars=self.candidates - 2) #hard coded for 3 candidates (might aswell put 1 tbh)

            else:
                minority_count = ((spare - i) + 1) * 2 #redundant brackets
                count = count + (self.stars_and_bars(stars=spare, bars=self.candidates - 2) - minority_count)

            i = i - 1
            spare = self.population - i

            if spare == 0:
                continue

            if round(spare / 2) >= i:
                break

        return count

    def get_direct_dist(self, neighbours): #for clough comparison
        votes = [0, 0, 0]
        for agent in neighbours:
            votes[agent.previous_vote_id] = votes[agent.previous_vote_id] + 1

        distribution = [round(vote / len(neighbours), 2) for vote in votes]
        return distribution

    def nCr(self, n, r): #binomial coefficient
        f = math.factorial
        return f(n) / f(r) / f(n-r)

    def stars_and_bars(self, stars, bars): #balls and urn technique
        return self.nCr(stars + bars, bars)

    def remaining(self, i, candidate, candidate_counts):
        remaining = i - candidate_counts[candidate]
        if remaining < 0:
            remaining = 0
        return remaining

    def liklihood(self, y, i, unobserved, candidate, candidate_counts): #liklihood function for bayesian step
        sample = unobserved
        remaining = self.remaining(i, candidate, candidate_counts)
        if y == candidate:
            return remaining / sample
        else:
            return (sample - remaining) / sample

    def bayesian_step(self, agent, marginal, unobserved, candidate, candidate_counts):

        y = agent.previous_vote_id

        top = [] #liklihood * prior for given x and y
        bottom = 0 #total liklihood x prior for given y

        for index in range(0, self.population + 1):
            sample = unobserved
            remaining = index - candidate_counts[candidate]
            if remaining < 0:
                remaining = 0
            if y == candidate:
                value = marginal[index] * (remaining / sample)
            else:
                value = marginal[index] * ((sample - remaining) / sample)
            top.append(value)
            bottom += value
        for index in range(0, self.population + 1):
            marginal[index] = top[index] / bottom

        return marginal

    def optimist_pmf(self, x, y, z): #where x is optimistic candidate
        if x > y and x > z:
            return 0.6 / self.win_events
        else:
            return 0.4 / (self.vote_events - self.win_events)

    def marginalise_distribution(self):

        x_marginal = []
        for x in range(0, self.population + 1):
            sum = 0
            for y in range(0, (self.population - x) + 1):
                z = (self.population - x) - y
                sum = sum + self.optimist_pmf(x, y, z)
            x_marginal.append(sum)

        return x_marginal

    def get_event_probability(self, candidate, marginal, ranges, x, y, z): #calculate an event probability using the conditional probability and the marginal distribution

        if candidate == 0:
            if marginal[x] == 0:
                return 0
            if y < ranges[1][0] or y > ranges[1][1]:
                return 0
            if z < ranges[2][0] or z > ranges[2][1]:
                return 0

            spare = self.population - x
            remaining_events = spare + 1
            for j in range(0, spare + 1):
                if (j < ranges[1][0] or j > ranges[1][1]) or (spare - j < ranges[2][0] or spare - j > ranges[2][1]):
                    remaining_events = remaining_events - 1

            return (1 / remaining_events) * marginal[x]

        if candidate == 1:
            if marginal[y] == 0:
                return 0
            if x < ranges[0][0] or x > ranges[0][1]:
                return 0
            if z < ranges[2][0] or z > ranges[2][1]:
                return 0

            spare = self.population - y
            remaining_events = spare + 1
            for j in range(0, spare + 1):
                if (j < ranges[0][0] or j > ranges[0][1]) or (spare - j < ranges[2][0] or spare - j > ranges[2][1]):
                    remaining_events = remaining_events - 1

            return (1 / remaining_events) * marginal[y]

        if candidate == 2:
            if marginal[z] == 0:
                return 0
            if x < ranges[0][0] or x > ranges[0][1]:
                return 0
            if y < ranges[1][0] or y > ranges[1][1]:
                return 0

            spare = self.population - z
            remaining_events = spare + 1
            for j in range(0, spare + 1):
                if (j < ranges[1][0] or j > ranges[1][1]) or (spare - j < ranges[0][0] or spare - j > ranges[0][1]):
                    remaining_events = remaining_events - 1

            return (1 / remaining_events) * marginal[z]

    def get_pivot_probabilities(self, neighbours): #interact with neighbourhood then calculate pivot probabilities

        observed = []
        unobserved = self.population
        marginal = self.marginalise_distribution() #construct marginal prior

        candidate = self.pure_vote_id
        candidate_counts = [0, 0, 0] #keeps counts of observed candidates for conditional probability function
        for agent in neighbours:
            bayesian_outcome = self.bayesian_step(agent=agent, marginal=marginal, unobserved=unobserved, candidate=candidate, candidate_counts=candidate_counts)
            observed.append(agent)
            candidate_counts[agent.previous_vote_id] = candidate_counts[agent.previous_vote_id] + 1
            unobserved = unobserved - 1
            marginal = bayesian_outcome

        #use marginal distribution to sum pivot probabilities
        pivot = {
            "01": 0,
            "12": 0,
            "02": 0
        }

        ranges = []
        for i in range(0, 3): #calculate the acceptable possible vote counts based on observations
            ranges.append([candidate_counts[i], self.population - (len(observed) - candidate_counts[i])])

        for i in range(0, math.floor(self.population / 2) + 1):
            remaining = self.population - (i * 2)
            if i + 1 < remaining - 1:
                continue
            pivot['01'] = pivot['01'] + self.get_event_probability(candidate=candidate, marginal=marginal,
                                                                   ranges=ranges, x=i, y=i, z=remaining)
            pivot['12'] = pivot['12'] + self.get_event_probability(candidate=candidate, marginal=marginal,
                                                                   ranges=ranges, x=remaining, y=i, z=i)
            pivot['02'] = pivot['02'] + self.get_event_probability(candidate=candidate, marginal=marginal,
                                                                   ranges=ranges, x=i, y=remaining, z=i)
        return pivot

    #prospective and utility methods

    def get_utility(self, party):
        return -1 * ((self.ideology - party.ideology)**2)

    def get_prospective_rating(self, party, pivot_probabilities, parties):
        rating = 0
        for p in parties:
            if p.id != party.id:
                if p.id < party.id:
                    key = str(p.id) + str(party.id)
                else:
                    key = str(party.id) + str(p.id)
                rating = rating + (pivot_probabilities[key] * (self.get_utility(party=party) - self.get_utility(party=p)))
        return rating

    #Interface methods
    def get_vote(self):
        return self.previous_vote_id

    def submit_vote(self):
        self.previous_vote_id = self.new_vote_id

    def choose_vote(self, parties, neighbours):
        pivot_probabilities = self.get_pivot_probabilities(neighbours=neighbours)
        #distribution = self.get_direct_dist(neighbours=neighbours)
        #pivot_probabilities = self.barycentric_system.get_pivot_probabilities(point=distribution)
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

    def pure_vote(self, parties): #Votes for party with highest utility based on ideology (Not a strategic vote).
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
        self.pure_vote_id = choice.id
        return choice
