class ImagePointFilter:
    def __init__(self, filter_radius):
        self.filter_radius = filter_radius
        self.occupied_point_list = []
        
    def get_point_distance_square(self, point1, point2):
        px, py = point1[0] - point2[0], point1[1] - point2[1]
        return (px ** 2 + py ** 2)
        
    def validate_point(self, point):
        for occupied_point in self.occupied_point_list:
            dist = self.get_point_distance_square(point, occupied_point)
            if dist <= self.filter_radius ** 2:
                return False
        self.occupied_point_list.append(point)
        return True
        
    def filter_points(self, point_list):
        return filter(self.validate_point, point_list)
