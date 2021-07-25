class Parameters:

    def __init__(self, mode):
        self.mode = mode

    def get_parameters(self):
        if self.mode == 1:
            return {
            "level": 1,
            "no_of_agents": 169,
            "no_of_parties": 3
            }
        elif self.mode == 2:
            return {
            "level": 2,
            "no_of_agents": 169,
            "no_of_parties": 3
            }

