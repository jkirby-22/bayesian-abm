class Parameters:

    def __init__(self, mode):
        self.mode = mode

    def get_parameters(self):
        if self.mode == 0:
            return {
            "id": 0,
            "level": 1,
            "no_agent": 169,
            "rounds": 1,
            "elections": 5,
            "no_party": 3
            }
        elif self.mode == 1:
            return {
            "id": 1,
            "level": 2,
            "no_agent": 169,
            "rounds": 1,
            "elections": 5,
            "no_party": 3
            }
        elif self.mode == 2: #changE!!!!
            return {
            "id": 2,
            "level": 6,
            "no_agent": 169,
            "rounds": 1,
            "elections": 5,
            "no_party": 3
            }

