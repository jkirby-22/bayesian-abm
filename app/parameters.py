class Parameters:

    def __init__(self, mode):
        self.mode = mode

    def get_parameters(self):
        if self.mode == 0:
            return {
            "id": 0,
            "level": 1,
            "no_agent": 169,
            "no_round": 50,
            "no_election": 5,
            "no_party": 3
            }
        if self.mode == 1:
            return {
            "id": 1,
            "level": 2,
            "no_agent": 169,
            "no_round": 50,
            "no_election": 5,
            "no_party": 3
            }
        if self.mode == 2:
            return {
            "id": 2,
            "level": 3,
            "no_agent": 169,
            "no_round": 50,
            "no_election": 5,
            "no_party": 3
            }
        if self.mode == 3:
            return {
            "id": 3,
            "level": 4,
            "no_agent": 169,
            "no_round": 50,
            "no_election": 5,
            "no_party": 3
            }
        if self.mode == 4:
            return {
            "id": 4,
            "level": 5,
            "no_agent": 169,
            "no_round": 50,
            "no_election": 5,
            "no_party": 3
            }
        if self.mode == 5:
            return {
            "id": 5,
            "level": 6,
            "no_agent": 169,
            "no_round": 50,
            "no_election": 5,
            "no_party": 3
            }

