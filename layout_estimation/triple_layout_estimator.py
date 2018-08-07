from . import LayoutUtils

class TripleLayoutEstimator:
    def __init__(self, pred_list, row_pred1, row_pred2, col_pred):
        self.pred_list = pred_list
        self.row_pred1 = row_pred1
        self.row_pred2 = row_pred2
        self.col_pred = col_pred
        self.letter_coord_map = {}
        self.layout_letter_dist = None

    def update_row_from_pred(self, row_pred):
        row_ind = LayoutUtils.get_letter_row_index(row_pred['letter'])
        if self.layout_letter_dist is None:
            raise Exception("Distance between letters is unknown")
        for letter in LayoutUtils.get_letters()[row_ind]:
            dir_dist = LayoutUtils.get_letter_dir_dist(row_pred['letter'], letter)
            letter_coord_map[letter] = row_pred['middle'] + self.layout_letter_dist * dir_dist

    def update_row_from_preds(self, row_pred1, row_pred2):
        row_ind1 = LayoutUtils.get_letter_row_index(row_pred1['letter'])
        row_ind2 = LayoutUtils.get_letter_row_index(row_pred2['letter'])
        if row_ind1 != row_ind2:
            raise Exception("Row predictions should have the same row number")
        letter_dist = LayoutUtils.get_letter_dist(row_pred1['letter'], row_pred2['letter'])
        self.layout_letter_dist = abs(row_pred1['middle'] - row_pred2['middle']) / letter_dist 
        self.update_row_from_pred(row_pred1)

    def update_row_from_angle(self, src_row_ind, dest_row_ind):
        src_letter = LayoutUtils.get_letters()[src_row_ind][0]
        dest_letter = LayoutUtils.get_letters()[dest_row_ind][0]
        src_coord = self.layout_coord_map[src_letter]
        dest_coord = ...
        self.letter_coord_map[dest_letter] = dest_coord
        for index, letter in enumerate(LayoutUtils.get_letters()[dest_row_ind][1:]):
            self.layout_coord_map[letter] = dest_coord + self.layout_letter_dist * index 

    def update_row_estimating_angle(self, src_row_ind, dest_row_ind, row_pred):
        pass#TODO

    def update_row_from_row(self, src_row_ind, dest_row_ind):
        col_row_ind =  LayoutUtils.get_letter_row_index(col_pred['letter'])
        if dest_row_ind == col_row_ind:
            self.update_row_estimating_angle(src_row_ind, dest_row_ind, self.col_pred)
        dest_filter_func = (lambda x: LayoutUtils.get_letter_row_index(x['letter']) == dest_row_ind)
        dest_preds = filter(dest_filter_func, self.pred_list)
        if len(dest_preds) == 0:
            self.update_row_from_angle(src_row_ind, dest_row_ind)
        else:
            sampled_pred = random.choice(dest_preds)
            self.update_row_estimating_angle(src_row_ind, dest_row_ind, sampled_pred)
    
    def estimate_lower_layouts(self, main_row_ind):
        for i in range(main_row + 1, len(LayoutUtils.get_letters())):
            self.update_row_from_row(i - 1, i)

    def estimate_upper_layouts(self, main_row_ind):
        for i in range(main_row - 1, 0, -1):
            self.update_row_from_row(i, i - 1)

    def estimate_layout(self, row_pred1, row_pred2, col_pred):
        if LayoutUtils.get_letter_pos(row_pred1) > LayoutUtils.get_letter_row_index(row_pred2):
            row_pred1, row_pred2 = row_pred2, row_pred1
        self.update_row_from_preds(row_pred1, row_pred2)
        main_row_ind = LayoutUtils.get_letter_row_index(row_pred1['letter'])
        col_row_ind =  LayoutUtils.get_letter_row_index(col_pred['letter'])
        if abs(col_row_ind - main_row_ind) != 1:
            raise Exception("Row predictions must be neighbours of col prediction")
        if col_row_ind - main_row_ind > 0:
            self.estimate_lower_layouts(main_row_ind)
            self.estimate_upper_layouts(main_row_ind)
        else:
            self.estimate_upper_layouts(main_row_ind)
            self.estimate_lower_layouts(main_row_ind)
