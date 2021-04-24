import math
class BayesianInference:
    def __init__(self):
        self.population = [1, 1, 1, 1, 2]
        self.step = 0
        v1_prior = [] #Optimistic cand
        for i in range(0, 6):
            v1_prior.append(self.optimist_pmf(i))
        self.v1_prior = v1_prior

        v2_prior = []
        for i in range(0, 6):
            v2_prior.append(self.skeptic_pmf(i))
        self.v2_prior = v2_prior

        #v3_prior = []
        #for i in range(0, 6):
            #v3_prior.append(self.skeptic_pmf(i))
       #self.v3_prior = v3_prior
    def optimist_pmf(self, i):
        population = len(self.population)
        majority = math.floor((population / 2) + 1)
        if i >= majority:
            return (1 / ((population + 1) - majority))
        else:
            return 0

    def skeptic_pmf(self, i):
        population = len(self.population)
        majority = math.floor((population / 2) + 1)
        if i < majority:
            return (1 / majority) #CHEKC THIS
        else:
            return 0

    def v1_liklihood(self, y, i):
        if y == 1:
            return i / 5 #change this!
        else:
            return (5 - i) / 5

    def v2_liklihood(self, y, i):
        if y == 2:
            return i / 5 #change this!
        else:
            return (5 - i) / 5

    def steps(self):
        y = self.population[0] #change
        top = []
        bottom = 0
        for index in range (0, 6):
            value = self.v1_prior[index] * self.v1_liklihood(y, index)
            top.append(value)
            bottom += value
        for index in range (0, 6):
            self.v1_prior[index] = top[index] / bottom

        top = []
        bottom = 0
        for index in range(0, 6):
            value = self.v2_prior[index] * self.v2_liklihood(y, index)
            top.append(value)
            bottom += value
        for index in range(0, 6):
            self.v2_prior[index] = top[index] / bottom


if __name__ == '__main__':
    inf = BayesianInference()
    print('Canditate 1 prior (optimist): ' + str(inf.v1_prior))
    print('Canditate 2 prior (skeptic): ' + str(inf.v2_prior))
    print(inf)
    inf.steps()
    print('Candidate 1 posterior: ' + str(inf.v1_prior))
    print('Candidate 2 posterior: ' + str(inf.v2_prior))
