import math
class BayesianInference:
    def __init__(self):
        self.population = [1, 3, 2]
        self.step = 0

        v1_prior = []
        for i in range(0, 6):
            v1_prior.append(self.optimist_pmf(i))
        self.v1_prior = v1_prior

        self.unobserved = self.population
        self.observed = []

    def remaining(self, i, candidate):
        count = 0
        for vote in self.observed:
            if vote == candidate:
                count += 1
        remaining = i - count
        if remaining < 0:
            remaining = 0
        return remaining

    def v1_liklihood(self, y, i):
        sample = len(self.unobserved)
        remaining = self.remaining(i, 1)
        if y == 1:
            return remaining / sample
        else:
            return (sample - remaining) / sample

    def v2_liklihood(self, y, i):
        sample = len(self.unobserved)
        remaining = self.remaining(i, 2)
        if y == 2:
            return remaining / sample
        else:
            return (sample - remaining) / sample

    def bayesian_step(self):
        y = self.unobserved[0] #change
        print('y: ' + str(y))
        top = [] #liklihood * prior for given x and y
        bottom = 0 #total liklihood x prior for given y

        #Candidate 1
        for index in range(0, 6):
            #g(index) * f(y | index)
            value = self.v1_prior[index] * self.v1_liklihood(y, index)
            top.append(value)
            bottom += value
        for index in range (0, 6):
            self.v1_prior[index] = top[index] / bottom

        #Candidate 2
        top = []
        bottom = 0
        for index in range(0, 6):
            value = self.v2_prior[index] * self.v2_liklihood(y, index)
            top.append(value)
            bottom += value
        for index in range(0, 6):
            self.v2_prior[index] = top[index] / bottom

        # Candidate 3
        top = []
        bottom = 0
        for index in range(0, 6):
            value = self.v3_prior[index] * self.v3_liklihood(y, index)
            top.append(value)
            bottom += value
        for index in range(0, 6):
            self.v3_prior[index] = top[index] / bottom

        # Candidate 3 (not v2)
        top = []
        bottom = 0
        for index in range(0, 6):
            value = self.v2_prior[index] * self.v2_liklihood(y, index)
            top.append(value)
            bottom += value
        for index in range(0, 6):
            self.v2_prior[index] = top[index] / bottom

        self.observed.append(self.unobserved.pop(0))
        print('Candidate 1 posterior: ' + str(inf.v1_prior))
        print('Candidate 2 posterior: ' + str(inf.v2_prior))
        print('Candidate 3 posterior: ' + str(inf.v3_prior))


if __name__ == '__main__':
    inf = BayesianInference()
    print('Canditate 1 prior (optimist): ' + str(inf.v1_prior))
    print('Canditate 2 prior (skeptic): ' + str(inf.v2_prior))
    print('Canditate 3 prior (skeptic): ' + str(inf.v3_prior))
    inf.bayesian_step()
    inf.bayesian_step()
    inf.bayesian_step()
    inf.bayesian_step()
    inf.bayesian_step()

