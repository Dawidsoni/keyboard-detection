from . import ImagePointFilter

class ImageFragmentFilter:
    def __init__(self, min_edge_size, max_edge_size, filter_radius=0):
        self.min_edge_size = min_edge_size
        self.max_edge_size = max_edge_size
        self.filter_radius = filter_radius
        self.image_point_filter = ImagePointFilter(filter_radius)
        
    def filter_fragments(self, fragment_list):
        edge_size_func = (lambda x: min(x[1].shape[0], x[1].shape[1]))
        fragment_list = filter(lambda x: edge_size_func(x) > self.min_edge_size, fragment_list)
        fragment_list = filter(lambda x: edge_size_func(x) < self.max_edge_size, fragment_list)
        if self.filter_radius == 0:
            return fragment_list
        point_list = map(lambda x: x[0], fragment_list)
        point_set = set(self.image_point_filter.filter_points(point_list))
        filtered_fragment_list = []
        for point, image in fragment_list:  
            if point in point_set:
                point_set.remove(point)
                filtered_fragment_list.append((point, image))
        return filtered_fragment_list
