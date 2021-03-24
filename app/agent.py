from party import Party
class Agent:
    def __init__(self, id, ideology):
        self.id = id
        self.ideology = ideology

    def vote(self, parties):
        difference = None
        choice = None
        for party in parties:
            current_difference = abs(self.ideology - party.ideology)
            if choice is None:
                choice = party
                difference = current_difference
            elif current_difference < difference:
                difference = current_difference
                choice = party

        return choice