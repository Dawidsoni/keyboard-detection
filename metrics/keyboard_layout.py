import pickle

class KeyboardLayout:
    def __init__(self, layout_file, min_scale=0.75, max_scale=5.0):
        layout_obj = pickle.load(open(layout_file, 'r'))
        self.layout_name = layout_obj['layout_name']
        self.layout_type = layout_obj['layout_type']
        self.letter_coords = layout_obj['letters']
        self.min_scale = min_scale
        self.max_scale = max_scale

    def _is_coord_in_middle(mid_coord, start_coord, end_coord):
        return all(lambda ind: mid_coord[ind] >= start_coord[ind] and mid_coord[ind] <= end_coord[ind], [0, 1])  

    def _is_inside_bounding_box(in_start_pos, in_end_pos, out_start_pos, out_end_pos):
        middle_func = (lambda x: _is_coord_in_middle(x, out_start_pos, out_end_pos))
        return middle_func(in_start_pos) and middle_func(in_end_pos)

    def _scale_bounding_box(start_pos, end_pos, scale):
        center_pos = tuple(map(lambda ind: (start_pos[ind] + end_pos[ind]) / 2, [0, 1]))
        diff_pos = tuple(map(lambda ind: (end_pos[ind] - start_pos[ind]) / 2, [0, 1]))
        scaled_start_pos = tuple(map(lambda ind: center_pos[ind] - diff_pos[ind] * scale, [0, 1]))
        scaled_end_pos = tuple(map(lambda ind: center_pos[ind] + diff_pos[ind] * scale, [0, 1]))
        return (scaled_start_pos, scaled_end_pos)

    def _is_inside_max_scaled_letter(letter_start_pos, letter_end_pos, start_pos, end_pos):
        letter_start_pos, letter_end_pos = _scale_bounding_box(letter_start_pos, letter_end_pos, self.max_scale)
        return _is_inside_bounding_box(start_pos, end_pos, letter_start_pos, letter_end_pos) 

    def _is_outside_min_scaled_letter(letter_start_pos, letter_end_pos, start_pos, end_pos):
        letter_start_pos, letter_end_pos = _scale_bounding_box(letter_start_pos, letter_end_pos, self.min_scale)
        return _is_inside_bounding_box(letter_start_pos, letter_end_pos, start_pos, end_pos)

    def find_letter(start_pos, end_pos):
        inside_func = (lambda x, y: _is_inside_max_scaled_letter(x, y, start_pos, end_pos)
        outside_func = (lambda x, y: _is_outside_min_scaled_letter(x, y, start_pos, end_pos)
        for coord in self.letter_coords:
            if inside_func(coord['start_pos'], coord['end_pos']) and outside_func(coord['start_pos', coord['end_pos'):
                return coord['letter']
        return ''
