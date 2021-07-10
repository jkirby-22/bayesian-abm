import math
class PriorConstructor:

    def __init__(self):
        self.population = 4
        self.candidates = 3
        self.vote_events = self.stars_and_bars(stars=self.population, bars=self.candidates - 1) #check
        self.win_events = self.get_win_events()

    def print_members(self):
        print('vote events: ' + str(self.vote_events))
        print('win events: ' + str(self.win_events))

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
            if round(spare / 2) >= i:
                break
        return count

if __name__ == '__main__':
    constructor = PriorConstructor()
    constructor.print_members()
#def optimist_pmf(self):
#0.6 / number of events in which x > y and y > z

