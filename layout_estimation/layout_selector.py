import numpy as np

class LayoutSelector:
    def __init__(self, pred_list):
        self.pred_list = pred_list

    @staticmethod
    def get_height_diff(layout, letter1, letter2):
        return abs(layout[letter1][1] - layout[letter2][1])

    @staticmethod
    def get_col_pbp(layout):
        diff_list = [('1', 'Q'), ('Q', 'A'), ('A', 'Z')]
        heights = map(lambda x: LayoutSelector.get_height_diff(layout, x[0], x[1]), diff_list)
        max_height = 0
        min_height = np.inf
        for i in range(len(heights)):
            for j in range(i + 1, len(heights)):
                max_height = max(max_height, abs(heights[i] - heights[j]))
                min_height = min(min_height, abs(heights[i] - heights[j]))
        return (float(min_height) / max_height)

    @staticmethod
    def is_point_in_middle(mid_point, start_point, end_point):
        coord_func = (lambda x: mid_point[x] >= start_point[x] and mid_point[x] <= end_point[x])
        return all(map(coord_func, [0, 1]))

    def rate_layout(self, layout):
        letter_pred_map = {}
        for pred in pred_list:
            letter_coord = tuple(layout[pred['letter']])
            start_pos, end_pos = pred['coord']['start_pos'], pred['coord']['end_pos']
            if letter_coord not in letter_pred_map:
                letter_pred_map[letter_coord] = 0
            if LayoutSelector.is_point_in_middle(letter_coord, start_pos, end_pos):
                letter_pred_map[letter_coord] = max(letter_pred_map[letter_coord], pred['pbp'])
        return LayoutSelector.get_col_rating(layout) * sum(letter_pred_map.values())
    
    def select_layout(self, layouts):
        return max(map(lambda x: (self.rate_layout(x), x), layouts))[1]
