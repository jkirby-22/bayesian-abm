import numpy as np

class Party:
    def __init__(self, id, parameters):
        self.id = id
        self.ideology = np.random.randint(1, 100) #sample ideology from a uniform distribution
        self.parameters = parameters
