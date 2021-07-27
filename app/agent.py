from party import Party
import math
from barycentric_system import BarycentricSystem
class Agent:
    def __init__(self, id, parameters):
        self.id = id
        self.ideology = None

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
            spare = self.population - i
            if i > spare:
                count = count + self.stars_and_bars(stars=spare, bars=self.candidates - 2) #hard coded for 3 candidates (might aswell put 1 tbh)

            else:
                minority_count = ((spare - i) + 1) * 2 #redundant brackets
                count = count + (self.stars_and_bars(stars=spare, bars=self.candidates - 2) - minority_count) #redundant brackets

            #fix this! bad code! just do the while loop maybe
            i = i - 1
            spare = self.population - i
            if spare == 0:
                continue
            #check for when rounded
            if round(spare / 2) >= i:
                break
        return count

    def nCr(self, n, r): #static?
        f = math.factorial
        return f(n) / f(r) / f(n-r)

    def stars_and_bars(self, stars, bars):
        return self.nCr(stars + bars, bars)

    def remaining(self, i, candidate, observed): #alot of variable passing here, maybe global is better tbh
        count = 0
        for agent in observed:
            if agent.previous_vote_id == candidate:
                count += 1
        remaining = i - count
        if remaining < 0:
            remaining = 0
        return remaining

    def liklihood(self, y, i, unobserved, observed, candidate):
        sample = unobserved
        remaining = self.remaining(i, candidate, observed)
        if y == candidate:
            return remaining / sample
        else:
            return (sample - remaining) / sample

    def bayesian_step(self, agent, marginal, unobserved, observed, candidate):

        y = agent.previous_vote_id #change notation

        top = [] #liklihood * prior for given x and y
        bottom = 0 #total liklihood x prior for given y

        for index in range(0, self.population + 1):
            value = marginal[index] * self.liklihood(y, index, unobserved, observed, candidate)
            top.append(value)
            bottom += value
        for index in range(0, self.population + 1):
            marginal[index] = top[index] / bottom

        return [marginal]

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
                z = (self.population - x) - y #redundant brackets
                sum = sum + self.optimist_pmf(x, y, z)
            x_marginal.append(sum)

        return x_marginal #change these names to optmist pesdsemist etc

    def get_event_probability(self, candidate, marginal, ranges, x, y, z):
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

    def get_pivot_probabilities(self, neighbours): #cant pass agents list as it shouldnt hav e access to that ygm?

        observed = []
        unobserved = self.population  #unobserved needs to be the whole pop overwise ou will just treat the distribution as direct anyway

        #construct marginal prior
        marginal = self.marginalise_distribution()

        candidate = self.pure_vote_id

        #bayesian steps
        for agent in neighbours:
            bayesian_outcome = self.bayesian_step(agent=agent, marginal=marginal, unobserved=unobserved, observed=observed, candidate=candidate)
            observed.append(agent)
            unobserved = unobserved - 1
            marginal = bayesian_outcome


        #use marginal distributions to sum pivot probabilities
        pivot = {
            "01": 0,
            "12": 0,
            "02": 0
        }

        candidate_counts = [0, 0, 0]
        for agent in observed:
            candidate_counts[agent.previous_vote_id] = candidate_counts[agent.previous_vote_id] + 1

        ranges = []
        for i in range(0, 3):
            ranges.append([candidate_counts[i], self.population - (len(observed) - candidate_counts[i])])

        for i in range(0, math.floor(self.population / 2)):
            remaining = self.population - (i * 2)
            pivot['01'] = pivot['01'] + self.get_event_probability(candidate=candidate, marginal=marginal,
                                                                   ranges=ranges, x=i, y=i, z=remaining)
            pivot['12'] = pivot['12'] + self.get_event_probability(candidate=candidate, marginal=marginal,
                                                                   ranges=ranges, x=remaining, y=i, z=i)
            pivot['02'] = pivot['02'] + self.get_event_probability(candidate=candidate, marginal=marginal,
                                                                   ranges=ranges, x=i, y=remaining, z=i)
        return pivot
    #prospective and utility methods
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

    #Interface methods
    def submit_vote(self):
        self.previous_vote_id = self.new_vote_id

    def choose_vote(self, parties, neighbours):
        pivot_probabilities = self.get_pivot_probabilities(neighbours=neighbours, no_of_parties=len(parties))
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
        #if self.id == 83:
            #print("Agent 83s vote: " + str(self.previous_vote_id))
        return choice
