import math
class PriorConstructor:

    def __init__(self):
        self.population = 3
        self.candidates = 3
        self.vote_events = self.stars_and_bars(stars=self.population, bars=self.candidates - 1) #check
        self.win_events = self.get_win_events()

        #assumes 3 candidates
        self.x_marginal = []
        self.y_marginal = []
        self.z_marginal = []

        self.marginalise_distributions()

    def print_members(self):
        print('vote events: ' + str(self.vote_events))
        print('win events: ' + str(self.win_events))
        print('x marginal: ' + str(self.x_marginal))
        print('y marginal: ' + str(self.y_marginal))
        print('z marginal: ' + str(self.z_marginal))

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
        events = []
        max_probability = 0
        #could potentially make this more effecient as loop over repeats
        for x in range(0, self.population + 1):
            for y in range(0, (self.population - x) + 1):
                z = (self.population - x) - y
                event_probability = (1 / self.stars_and_bars(stars=self.population - x, bars=self.candidates - 2)) * self.x_marginal[x]
                if event_probability > max_probability:
                    events = [x, y, z]
                    max_probability = event_probability

                elif event_probability == max_probability:
                    events.append([x, y, z])

        return [events, max_probability]


if __name__ == '__main__':
    constructor = PriorConstructor()
    constructor.print_members()
    print(constructor.get_most_likely_events())


#0.6 / number of events in which x > y and y > z

