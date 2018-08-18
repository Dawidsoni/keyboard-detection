from . import LayoutUtils

class TriplesProducer:
    def __init__(self, pred_list):
        self.pred_list = pred_list
        self.triples = None

    def create_row_preds_map(self):
        row_preds_map = {}
        for pred in self.pred_list:
            row_ind = LayoutUtils.get_letter_row_index(pred['letter'])
            pos_ind = LayoutUtils.get_letter_pos(pred['letter'])
            if row_ind not in row_preds_map:
                row_preds_map[row_ind] = {}
            if pos_ind not in row_preds_map[row_ind]:
                row_preds_map[row_ind][pos_ind] = []
            row_preds_map[row_ind][pos_ind].append(pred)    
        return row_preds_map

    def add_triples_for_row(self, row_preds_map, row_ind, pos1, pos2, row_offset):
        neigh_row = row_ind + row_offset
        if neigh_row not in row_preds_map:
            return
        for row_pred1 in row_preds_map[row_ind][pos1]:
            for row_pred2 in row_preds_map[row_ind][pos2]:
                neigh_preds = row_preds_map[neigh_row].values()
                for col_pred in [x for sublist in neigh_preds for x in sublist]:
                    col_pos = LayoutUtils.get_letter_pos(col_pred['letter'])
                    if col_pos > len(LayoutUtils.get_letter_rows()[row_ind]) - 1:
                        continue
                    self.triples.append((row_pred1, row_pred2, col_pred)) 

    def produce_triples(self):
        row_preds_map = self.create_row_preds_map()
        self.triples = []
        for row_ind in row_preds_map.keys():
            for pos1 in row_preds_map[row_ind].keys():
                for pos2 in row_preds_map[row_ind].keys():
                    if pos1 + 3 > pos2:
                        continue
                    self.add_triples_for_row(row_preds_map, row_ind, pos1, pos2, -1)
                    self.add_triples_for_row(row_preds_map, row_ind, pos1, pos2, 1) 
        return self.triples

    def get_triples(self):
        if self.triples is None:
            self.triples = self.produce_triples()
        return self.triples
