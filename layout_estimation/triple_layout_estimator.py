import random
from . import LayoutUtils

class TripleLayoutEstimator:
    def __init__(self, pred_list, row_pred1, row_pred2, col_pred):
        self.pred_list = pred_list
        self.row_pred1 = row_pred1
        self.row_pred2 = row_pred2
        self.col_pred = col_pred
        self.letter_coord_map = {}
        self.layout_letter_dist = None
        self.row_offset = None

    def update_row_from_pred(self, row_pred):
        row_ind = LayoutUtils.get_letter_row_index(row_pred['letter'])
        if self.layout_letter_dist is None:
            raise Exception("Distance between letters is unknown")
        for letter in LayoutUtils.get_letter_rows()[row_ind]:
            dir_dist = LayoutUtils.get_letter_dir_dist(letter, row_pred['letter'])
            self.letter_coord_map[letter] = row_pred['middle'] + self.layout_letter_dist * dir_dist

    def update_row_from_preds(self, row_pred1, row_pred2):
        row_ind1 = LayoutUtils.get_letter_row_index(row_pred1['letter'])
        row_ind2 = LayoutUtils.get_letter_row_index(row_pred2['letter'])
        if row_ind1 != row_ind2:
            raise Exception("Row predictions should have the same row number")
        letter_dist = LayoutUtils.get_letter_dist(row_pred1['letter'], row_pred2['letter'])
        self.layout_letter_dist = (row_pred1['middle'] - row_pred2['middle']) / letter_dist 
        self.update_row_from_pred(row_pred1)

    def update_row_from_angle(self, src_row_ind, dst_row_ind):
        if self.row_offset is None:
            raise Exception("Row offset is not specified")
        src_letter = LayoutUtils.get_letters()[src_row_ind][0]
        dst_letter = LayoutUtils.get_letters()[dst_row_ind][0]
        src_coord = self.letter_coord_map[src_letter]
        dst_coord = src_coord + self.row_offset * (src_row_ind - dst_row_ind)
        for index, letter in enumerate(LayoutUtils.get_letter_rows()[dst_row_ind]):
            self.layout_coord_map[letter] = dst_coord + self.layout_letter_dist * index 

    def update_row_estimating_angle(self, src_row_ind, dst_row_ind, row_pred):
        letter_pos = LayoutUtils.get_letter_pos(row_pred['letter'])
        src_letter = LayoutUtils.get_letter_rows()[src_row_ind][letter_pos]
        src_coord = self.letter_coord_map[src_letter]
        self.row_offset = (row_pred['middle'] - src_coord) * (src_row_ind - dst_row_ind)
        dst_coord = src_coord + (self.row_offset * (src_row_ind - dst_row_ind))
        for index, letter in enumerate(LayoutUtils.get_letter_rows()[dst_row_ind]):
            dir_dist = LayoutUtils.get_letter_dir_dist(letter, row_pred['letter'])
            self.letter_coord_map[letter] = dst_coord + self.layout_letter_dist * dir_dist

    def update_row_from_row(self, src_row_ind, dst_row_ind):
        col_row_ind =  LayoutUtils.get_letter_row_index(self.col_pred['letter'])
        if dst_row_ind == col_row_ind:
            self.update_row_estimating_angle(src_row_ind, dst_row_ind, self.col_pred)
            return
        max_pos = len(LayoutUtils.get_letter_rows()[src_row_ind]) - 1
        row_filter_func = (lambda x: LayoutUtils.get_letter_row_index(x['letter']) == dst_row_ind)
        len_filter_func = (lambda x: LayoutUtils.get_letter_pos(x["letter"]) <= max_pos)
        dst_preds = filter(lambda x: row_filter_func(x) and len_filter_func(x), self.pred_list)
        if len(dst_preds) == 0:
            self.update_row_from_angle(src_row_ind, dst_row_ind)
        else:
            sampled_pred = random.choice(dst_preds)
            self.update_row_estimating_angle(src_row_ind, dst_row_ind, sampled_pred)
    
    def estimate_lower_layouts(self, main_row_ind):
        for i in range(main_row_ind + 1, len(LayoutUtils.get_letter_rows())):
            self.update_row_from_row(i - 1, i)

    def estimate_upper_layouts(self, main_row_ind):
        for i in range(main_row_ind, 0, -1):
            self.update_row_from_row(i, i - 1)

    def get_estimated_layout(self):
        pred1_pos = LayoutUtils.get_letter_pos(self.row_pred1['letter'])
        pred2_pos = LayoutUtils.get_letter_pos(self.row_pred2['letter'])
        if pred1_pos < pred2_pos:
            self.row_pred1, self.row_pred2 = self.row_pred2, self.row_pred1
        self.update_row_from_preds(self.row_pred1, self.row_pred2)
        main_row_ind = LayoutUtils.get_letter_row_index(self.row_pred1['letter'])
        col_row_ind =  LayoutUtils.get_letter_row_index(self.col_pred['letter'])
        if abs(col_row_ind - main_row_ind) != 1:
            raise Exception("Row predictions must be neighbours of col prediction")
        if col_row_ind - main_row_ind > 0:
            self.estimate_lower_layouts(main_row_ind)
            self.estimate_upper_layouts(main_row_ind)
        else:
            self.estimate_upper_layouts(main_row_ind)
            self.estimate_lower_layouts(main_row_ind)
        return self.letter_coord_map
