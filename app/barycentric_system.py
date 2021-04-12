import numpy as np
class BarycentricSystem: #camel case for file name?

    def __init__(self):
        self.dimension = 3

    def get_draw_point(self, point, control_index): #REMOVE LOOOP!
        new_point = []
        for i in range(0, self.dimension): #maybe dont make this loop and have it have samme interface to the checks?
            if i == control_index:
                new_point.append(point[control_index])
            else:
                new_point.append((1 - point[control_index]) / 2)
        return new_point

    #def get_sp(self, point, index_one, index_two):
        #eucliedan = (((point[index_one] / 2) ** 2) + ((point[index_two] / 2) ** 2) - (point[index_one] * point[index_two])) ** 0.5
        #print(eucliedan)
        #return 1 - eucliedan

    #def get_mp(self, point):
        #eucliedan = (2 / 3 * ((point[0] ** 2) + (point[1] ** 2) + (point[2] ** 2) - (point[0] * point[1]) - (point[0] * point[2]) - (point[1] * point[2]))) ** 0.5
        #return 1 - eucliedan

    def get_mp(self, point):
        return 1 - np.linalg.norm(point - np.asarray([0.33, 0.33, 0.33]))

    def get_sp(self, point, control_index):
        draw_point = self.get_draw_point(point, control_index)
        return 1 - np.linalg.norm(np.asarray(point) - np.asarray(draw_point))


    def second_third_tie_check(self, point, index_one, index_two, control_index):
        if point[control_index] > point[index_one] and point[control_index] > point[index_two]:
            return True
        else:
            return False

    def dominant_second_finish_check(self, point, index_one, index_two, control_index):
        average = (point[index_one] + point[index_two]) / 2
        if point[control_index] > average:
            return True
        else:
            return False

    def get_pivot_probabilities(self, point):
        #Should do comibinations formulae here if want to extend to 4
        #return dict for extensibilities sake
        pivot = { #not extensible
            "01": 0,
            "02": 0,
            "12": 0
        }
        if point[0] == point[1] == point[2]: #if all equal then just return constant so utility is used. This ISNT MODULAR THO AS UTILITY OUTSIDE OF PROB SCOPE
            pivot["01"] = 1
            pivot["02"] = 1
            pivot["12"] = 1

        mp = self.get_mp(point=point)
        #p12
        index_one = 0
        index_two = 1
        control_index = 2
        if self.second_third_tie_check(point=point, index_one=index_one, index_two=index_two, control_index=control_index) or self.dominant_second_finish_check(point=point, index_one=index_one, index_two=index_two, control_index=control_index):
            p12 = mp
        else:
            p12 = self.get_sp(point=point, control_index=control_index)

        #p13
        index_one = 0
        index_two = 2
        control_index = 1
        if self.second_third_tie_check(point=point, index_one=index_one, index_two=index_two, control_index=control_index) or self.dominant_second_finish_check(point=point, index_one=index_one, index_two=index_two, control_index=control_index):
            p13 = mp
        else:
            p13 = self.get_sp(point=point, control_index=control_index)

        #p23
        index_one = 1
        index_two = 2
        control_index = 0
        if self.second_third_tie_check(point=point, index_one=index_one, index_two=index_two,control_index=control_index) or self.dominant_second_finish_check(point=point, index_one=index_one, index_two=index_two, control_index=control_index):
            p23 = mp
        else:
            p23 = self.get_sp(point=point, control_index=control_index)

        pivot["01"] = round(p12, 2)
        pivot["02"] = round(p13, 2)
        pivot["12"] = round(p23, 2)
        return pivot