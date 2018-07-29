from . import ImagePointFilter

class ImageFragmentFilter:
    def __init__(self, image, extract_params, filter_radius=None):
        self.image = image
        self.extract_params = extract_params
        self.filter_radius = filter_radius

    def get_min_fragment_size(self):
        return int(max(self.image.shape[0], self.image.shape[1]) / self.extract_params.min_scale)

    def get_max_fragment_size(self):
        return int(max(self.image.shape[0], self.image.shape[1]) / self.extract_params.max_scale)

    def filter_fragments(self, fragment_list):
        min_fragment_size = self.get_min_fragment_size()
        max_fragment_size = self.get_max_fragment_size()
        min_edge_size_func = (lambda x: min(x[1].shape[0], x[1].shape[1]))
        max_edge_size_func = (lambda x: max(x[1].shape[0], x[1].shape[1]))
        fragment_list = filter(lambda x: min_edge_size_func(x) > min_fragment_size, fragment_list)
        fragment_list = filter(lambda x: max_edge_size_func(x) < max_fragment_size, fragment_list)
        if self.filter_radius is None:
            return fragment_list
        point_list = map(lambda x: x[0], fragment_list)
        point_set = set(self.image_point_filter.filter_points(point_list))
        filtered_fragment_list = []
        for point, image in fragment_list:  
            if point in point_set:
                point_set.remove(point)
                filtered_fragment_list.append((point, image))
        return filtered_fragment_list
