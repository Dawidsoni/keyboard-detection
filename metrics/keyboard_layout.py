import pickle
import string
import cv2

class KeyboardLayout:
    STABLE_LAYOUT = "stable"
    ROTATED_LAYOUT = "rotated"

    def __init__(self, layout_file, path_prefix='', min_scale=0.9, max_scale=4.0):
        layout_obj = pickle.load(open(layout_file, 'r'))
        self.layout_name = layout_obj['layout_name']
        self.layout_path = layout_obj['filepath']
        self.layout_type = layout_obj['layout_type']
        self.letter_coords = layout_obj['letters']
        self.path_prefix = path_prefix
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.cached_image = None

    @staticmethod
    def get_layout_chars():
        return string.ascii_uppercase + string.digits

    @staticmethod
    def _is_point_in_middle(mid_point, start_point, end_point):
        coord_func = (lambda x: mid_point[x] >= start_point[x] and mid_point[x] <= end_point[x])
        return all(map(coord_func, [0, 1]))

    @staticmethod
    def _is_inside_bounding_box(in_start_pos, in_end_pos, out_start_pos, out_end_pos):
        middle_func = (lambda x: KeyboardLayout._is_point_in_middle(x, out_start_pos, out_end_pos))
        return middle_func(in_start_pos) and middle_func(in_end_pos)

    @staticmethod
    def _scale_bounding_box(start_pos, end_pos, scale):
        center_pos = tuple(map(lambda ind: (start_pos[ind] + end_pos[ind]) / 2, [0, 1]))
        diff_pos = tuple(map(lambda ind: (end_pos[ind] - start_pos[ind]) / 2, [0, 1]))
        scaled_start_pos = tuple(map(lambda ind: center_pos[ind] - diff_pos[ind] * scale, [0, 1]))
        scaled_end_pos = tuple(map(lambda ind: center_pos[ind] + diff_pos[ind] * scale, [0, 1]))
        return (scaled_start_pos, scaled_end_pos)

    def _is_inside_max_scaled_letter(self, lett_start_pos, lett_end_pos, start_pos, end_pos):
        sc_start_pos, sc_end_pos = KeyboardLayout._scale_bounding_box(lett_start_pos, lett_end_pos, self.max_scale)
        return KeyboardLayout._is_inside_bounding_box(start_pos, end_pos, sc_start_pos, sc_end_pos) 

    def _is_outside_min_scaled_letter(self, lett_start_pos, lett_end_pos, start_pos, end_pos):
        sc_start_pos, sc_end_pos = KeyboardLayout._scale_bounding_box(lett_start_pos, lett_end_pos, self.min_scale)
        return KeyboardLayout._is_inside_bounding_box(sc_start_pos, sc_end_pos, start_pos, end_pos)

    def find_letter(self, start_pos, end_pos):
        inside_func = (lambda x, y: self._is_inside_max_scaled_letter(x, y, start_pos, end_pos))
        outside_func = (lambda x, y: self._is_outside_min_scaled_letter(x, y, start_pos, end_pos))
        for coord in self.letter_coords:
            if inside_func(coord['start_pos'], coord['end_pos']) and outside_func(coord['start_pos'], coord['end_pos']):
                return coord['letter']
        return None

    def is_stable_layout(self):
        return self.layout_type == KeyboardLayout.STABLE_LAYOUT

    def is_rotated_layout(self):
        return self.layout_type == KeyboardLayout.ROTATED_LAYOUT

    def get_image(self):
        if self.cached_image is None:
            self.cached_image = cv2.imread(self.path_prefix + self.layout_path, 1)
        return self.cached_image
