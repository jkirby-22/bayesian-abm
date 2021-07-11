import math
class PriorConstructor:

    def __init__(self):

        self.population_votes = [1, 2, 3]
        self.population = len(self.population_votes)
        self.candidates = 3
        self.vote_events = self.stars_and_bars(stars=self.population, bars=self.candidates - 1) #check
        self.win_events = self.get_win_events()

        #assumes 3 candidates
        self.x_marginal = []
        self.y_marginal = []
        self.z_marginal = []

        self.unobserved = self.population_votes
        self.observed = []

        self.marginalise_distributions()

    def print_members(self):
        print('vote events: ' + str(self.vote_events))
        print('win events: ' + str(self.win_events))
        print('x marginal: ' + str(self.x_marginal))
        print('y marginal: ' + str(self.y_marginal))
        print('z marginal: ' + str(self.z_marginal))

    def remaining(self, i, candidate):
        count = 0
        for vote in self.observed:
            if vote == candidate:
                count += 1
        remaining = i - count
        if remaining < 0:
            remaining = 0
        return remaining

    def x_liklihood(self, y, i):
        sample = len(self.unobserved)
        remaining = self.remaining(i, 1)
        if y == 1:
            return remaining / sample
        else:
            return (sample - remaining) / sample

    def y_liklihood(self, y, i):
        sample = len(self.unobserved)
        remaining = self.remaining(i, 2)
        if y == 2:
            return remaining / sample
        else:
            return (sample - remaining) / sample

    def z_liklihood(self, y, i):
        sample = len(self.unobserved)
        remaining = self.remaining(i, 3)
        if y == 3:
            return remaining / sample
        else:
            return (sample - remaining) / sample

    def bayesian_step(self):
        y = self.unobserved[0] #change
        #print('y: ' + str(y))
        top = [] #liklihood * prior for given x and y
        bottom = 0 #total liklihood x prior for given y

        #Candidate 1
        for index in range(0, self.population + 1):
            value = self.x_marginal[index] * self.x_liklihood(y, index)
            top.append(value)
            bottom += value
        for index in range(0, self.population + 1):
            self.x_marginal[index] = top[index] / bottom

        #Candidate 2
        top = []
        bottom = 0
        for index in range(0, self.population + 1):
            value = self.y_marginal[index] * self.y_liklihood(y, index)
            top.append(value)
            bottom += value
        for index in range(0, self.population + 1):
            self.y_marginal[index] = top[index] / bottom

        # Candidate 3
        top = []
        bottom = 0
        for index in range(0, self.population + 1):
            value = self.z_marginal[index] * self.z_liklihood(y, index)
            top.append(value)
            bottom += value
        for index in range(0, self.population + 1):
            self.z_marginal[index] = top[index] / bottom

        self.observed.append(self.unobserved.pop(0))
        print('Candidate x posterior: ' + str(self.x_marginal))
        print('Candidate y posterior: ' + str(self.y_marginal))
        print('Candidate z posterior: ' + str(self.z_marginal))

    def nCr(self, n, r):
        f = math.factorial
        return f(n) / f(r) / f(n-r)

    def stars_and_bars(self, stars, bars):
        return self.nCr(stars + bars, bars)

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

    def optimist_pmf(self, x, y, z): #where x is optimistic candidate
        if x > y and x > z:
            return 0.6 / self.win_events
        else:
            return 0.4 / (self.vote_events - self.win_events)

    def standard_pmf(self):
        return 1 / self.vote_events

    def marginalise_distributions_standard(self):

        for x in range(0, self.population + 1):
            sum = 0
            for y in range(0, (self.population - x) + 1):
                z = (self.population - x) - y #redundant brackets
                sum = sum + self.standard_pmf()
            self.x_marginal.append(sum)

        #NEED TO CHECK THE Y AND Z MARGINALS!
        for y in range(0, self.population + 1):
            sum = 0
            for z in range(0, (self.population - y) + 1):
                x = (self.population - y) - z #redundant brackets
                sum = sum + self.standard_pmf()
            self.y_marginal.append(sum)

        for z in range(0, self.population + 1):
            sum = 0
            for x in range(0, (self.population - z) + 1):
                y = (self.population - z) - x #redundant brackets
                sum = sum + self.standard_pmf()
            self.z_marginal.append(sum)

    def marginalise_distributions(self):

        for x in range(0, self.population + 1):
            sum = 0
            for y in range(0, (self.population - x) + 1):
                z = (self.population - x) - y #redundant brackets
                sum = sum + self.optimist_pmf(x, y, z)
            self.x_marginal.append(sum)

        #NEED TO CHECK THE Y AND Z MARGINALS!
        for y in range(0, self.population + 1):
            sum = 0
            for z in range(0, (self.population - y) + 1):
                x = (self.population - y) - z #redundant brackets
                sum = sum + self.optimist_pmf(x, y, z)
            self.y_marginal.append(sum)

        for z in range(0, self.population + 1):
            sum = 0
            for x in range(0, (self.population - z) + 1):
                y = (self.population - z) - x #redundant brackets
                sum = sum + self.optimist_pmf(x, y, z)
            self.z_marginal.append(sum)

    def get_most_likely_events(self):
        sum = 0
        events = []
        max_probability = 0
        for x in range(0, self.population + 1):
            if self.x_marginal[x] == 0:
                continue
            for y in range(0, (self.population - x) + 1):
                if self.y_marginal[y] == 0:
                    continue

                z = (self.population - x) - y
                if self.z_marginal[z] == 0:
                    continue

                remaining_events = (self.population - x) + 1 #redundant brackets
                for i in range(0, (self.population - x) + 1):
                    if self.y_marginal[i] == 0:
                        remaining_events = remaining_events - 1

                event_probability = (1 / remaining_events) * self.x_marginal[x]
                sum = sum + event_probability
                if event_probability > max_probability:
                    events = [x, y, z]
                    max_probability = event_probability

                elif event_probability == max_probability:
                    events.append([x, y, z])

        print(sum)
        return [events, max_probability]


if __name__ == '__main__':
    constructor = PriorConstructor()
    constructor.print_members()
    constructor.bayesian_step()
    print(constructor.get_most_likely_events())
    constructor.bayesian_step()
    print(constructor.get_most_likely_events())
    constructor.bayesian_step()
    print(constructor.get_most_likely_events())


#0.6 / number of events in which x > y and y > z

