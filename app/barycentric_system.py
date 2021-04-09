class BarycentricSystem: #camel case for file name?

    def __init__(self):
        self.dimension = 3

    def get_max_pairwise_point(self, point, control_index):
        new_point = []
        for i in range(0, self.dimension):
            if i == control_index:
                new_point.append(point[control_index])
            else:
                new_point.append((1 - point[control_index]) / 2)
        return new_point

    def get_draw_point(self, point, control_index):
        #logic here to check if min or max
        return self.get_max_pairwise_point(point=point, control_index=control_index)
