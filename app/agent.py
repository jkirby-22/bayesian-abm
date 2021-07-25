from party import Party
from environment import Environment
import math
from barycentric_system import BarycentricSystem
class Agent:
    def __init__(self, id):
        self.id = id
        self.ideology = None

        self.previous_vote_id = None
        self.new_vote_id = None
        self.pure_vote_id = None

        self.barycentric_system = BarycentricSystem()  # just for effeciency to not create a new one evverytime

        self.population = 168 #probably need to clean this up (excluding ya self because we calculate vote shhare without us)
        self.candidates = 3 #CLEAN UP!!
        self.vote_events = self.stars_and_bars(stars=self.population, bars=self.candidates - 1) #might need to put in another file
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

    def x_liklihood(self, y, i, unobserved, observed):
        sample = unobserved
        remaining = self.remaining(i, 0, observed)
        if y == 0:
            return remaining / sample
        else:
            return (sample - remaining) / sample

    def y_liklihood(self, y, i, unobserved, observed):
        sample = unobserved
        remaining = self.remaining(i, 1, observed)
        if y == 1:
            return remaining / sample
        else:
            return (sample - remaining) / sample

    def z_liklihood(self, y, i, unobserved, observed): #change to v3 etc!!!!!!
        sample = unobserved
        remaining = self.remaining(i, 2, observed)
        if y == 2:
            return remaining / sample
        else:
            return (sample - remaining) / sample

    def bayesian_step(self, agent, x_marginal, y_marginal, z_marginal, unobserved, observed):

        y = agent.previous_vote_id #change

        top = [] #liklihood * prior for given x and y
        bottom = 0 #total liklihood x prior for given y

        #Candidate x
        for index in range(0, self.population + 1):
            value = x_marginal[index] * self.x_liklihood(y, index, unobserved, observed)
            top.append(value)
            bottom += value
        for index in range(0, self.population + 1):
            x_marginal[index] = top[index] / bottom

        #Candidate y
        top = []
        bottom = 0
        for index in range(0, self.population + 1):
            value = y_marginal[index] * self.y_liklihood(y, index, unobserved, observed)
            top.append(value)
            bottom += value
        for index in range(0, self.population + 1):
            y_marginal[index] = top[index] / bottom

        # Candidate z
        top = []
        bottom = 0
        for index in range(0, self.population + 1):
            value = z_marginal[index] * self.z_liklihood(y, index, unobserved, observed)
            top.append(value)
            bottom += value
        for index in range(0, self.population + 1):
            z_marginal[index] = top[index] / bottom

        return [x_marginal, y_marginal, z_marginal]

    def optimist_pmf(self, x, y, z): #where x is optimistic candidate
        if x > y and x > z:
            return 0.6 / self.win_events
        else:
            return 0.4 / (self.vote_events - self.win_events)

    def marginalise_distributions(self):

        x_marginal = []
        y_marginal = []
        z_marginal = []

        for x in range(0, self.population + 1):
            sum = 0
            for y in range(0, (self.population - x) + 1):
                z = (self.population - x) - y #redundant brackets
                sum = sum + self.optimist_pmf(x, y, z)
            x_marginal.append(sum)

        #NEED TO CHECK THE Y AND Z MARGINALS!
        for y in range(0, self.population + 1):
            sum = 0
            for z in range(0, (self.population - y) + 1):
                x = (self.population - y) - z #redundant brackets
                sum = sum + self.optimist_pmf(x, y, z)
            y_marginal.append(sum)

        for z in range(0, self.population + 1):
            sum = 0
            for x in range(0, (self.population - z) + 1):
                y = (self.population - z) - x #redundant brackets
                sum = sum + self.optimist_pmf(x, y, z)
            z_marginal.append(sum)

        return [x_marginal, y_marginal, z_marginal] #change these names to optmist pesdsemist etc

    def get_most_likely_events(self, x_marginal, y_marginal, z_marginal):
        sum = 0
        events = []
        max_probability = 0
        for x in range(0, self.population + 1):
            if x_marginal[x] == 0:
                continue
            for y in range(0, (self.population - x) + 1):
                if y_marginal[y] == 0:
                    continue

                z = (self.population - x) - y
                if z_marginal[z] == 0:
                    continue

                remaining_events = (self.population - x) + 1 #redundant brackets
                for i in range(0, (self.population - x) + 1):
                    if y_marginal[i] == 0:
                        remaining_events = remaining_events - 1

                event_probability = (1 / remaining_events) * x_marginal[x]
                sum = sum + event_probability
                if event_probability > max_probability:
                    events = [[x, y, z]]
                    max_probability = event_probability

                elif event_probability == max_probability:
                    events.append([x, y, z])

        #print('Probability sum ' + str(sum))
        #print(events)
        return [events, max_probability]

    def get_direct_dist(self, environment, level):
        votes = [0, 0, 0]  # change more modular
        neighbours = environment.get_neighbour_agents(agent_id=self.id, level=level)
        for agent in neighbours:
            votes[agent.previous_vote_id] = votes[agent.previous_vote_id] + 1  # (1 / len(neighbours)) CANT DO THIS FOR SOME REASON EVEN THO MORE EFFECIENT?
        distribution = [round(vote / len(neighbours), 2) for vote in votes]
        return distribution
    def get_probability_distribution(self, neighbours, no_of_parties): #cant pass agents list as it shouldnt hav e access to that ygm?

        #if self.id == 0:
            #print('Agent: ' + str(self.id))
            #print('Pure vote: ' + str(self.pure_vote_id))

        observed = []
        unobserved = self.population  #unobserved needs to be the whole pop overwise ou will just treat the distribution as direct anyway

        #construct marginal priors
        marginals = self.marginalise_distributions()

        #PRETTY SUrE MARGINALS FOR 1 AND 2 ARE JSUT DUPLICATES SO CAN CLEAN THAT UP!!
        if self.pure_vote_id == 0:
            # CHANGE THESE TO V1, V2 ETC
            x_marginal = marginals[0]
            y_marginal = marginals[1]
            z_marginal = marginals[2]

        if self.pure_vote_id == 1:
            # CHANGE THESE TO V1, V2 ETC
            x_marginal = marginals[1]
            y_marginal = marginals[0]
            z_marginal = marginals[2]

        if self.pure_vote_id == 2:
            # CHANGE THESE TO V1, V2 ETC
            x_marginal = marginals[1]
            y_marginal = marginals[2]
            z_marginal = marginals[0]

        #bayesian steps
        count = 0
        for agent in neighbours:
            bayesian_outcome = self.bayesian_step(agent=agent, x_marginal=x_marginal, y_marginal=y_marginal, z_marginal=z_marginal, unobserved=unobserved, observed=observed)
            observed.append(agent)
            unobserved = unobserved - 1
            x_marginal = bayesian_outcome[0]
            y_marginal = bayesian_outcome[1]
            z_marginal = bayesian_outcome[2]
            #print(count)
            count = count + 1
        if self.id == 0:
            x = 0
            y = 0
            z = 0
            count = 0
            #print(self.get_most_likely_events(x_marginal, y_marginal, z_marginal)[0][0])


            for x in x_marginal:
                #print(x)
                if int(x) == 1:
                    #print('true')
                    x = count
                    break
                count = count + 1
            #print(x)

            count = 0
            for x in y_marginal:
                if int(x) == 1:
                    y = count
                    break
                count = count + 1
            #print(y)

            count = 0
            for x in z_marginal:
                if int(x) == 1:
                    z = count
                    break
                count = count + 1
            #print(z)
        #uncompact marginals to get most likely events
        events = self.get_most_likely_events(x_marginal, y_marginal, z_marginal)[0]

        largest_share = 0
        optimal_event = None
        for event in events:
            percentage = [event[0] / 168, event[1] / 168, event[2] / 168]
            if percentage[self.pure_vote_id] >= largest_share:
                optimal_event = event
                largest_share = percentage[self.pure_vote_id]

        optimal_event_share = [optimal_event[0] / 168, optimal_event[1] / 168, optimal_event[2] / 168] #HARDCODED FOR 168!!
        #if self.id == 0:
            #print('Preffered candidate: ' + str(self.pure_vote_id))
           #print('Bayesian: ')
            #print(optimal_event_share)
            #print('Direct: ')
            #print(self.get_direct_dist(environment, level))
        return optimal_event_share #Need to calculate the most likely event out of list not just take the first item

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

    def choose_vote(self, parties, neighbours, level):
        distribution = self.get_probability_distribution(neighbours=neighbours, no_of_parties=len(parties))
        pivot_probabilities = self.barycentric_system.get_pivot_probabilities(point=distribution)

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
