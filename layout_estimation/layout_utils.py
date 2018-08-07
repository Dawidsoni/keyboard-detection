class LayoutUtils:
    LETTER_ROWS = ['1234567890', 'QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM']

    @staticmethod
    def get_row_letters_map():
        return {i: LayoutUtils.LETTER_ROWS[i] for i in range(len(LayoutUtils.LETTER_ROWS))}

    @staticmethod
    def get_letter_row_index(letter):
        ind_list =  filter(lambda i: letter in LayoutUtils.LETTER_ROWS[i], range(len(LayoutUtils.LETTER_ROWS)))
        if len(ind_list) == 0:
            raise Exception("Letter not found")
        return ind_list[0]

    @staticmethod
    def get_letter_pos(letter):
        row_ind = LayoutUtils.get_letter_row_index(letter)
        return LayoutUtils.LETTER_ROWS[row_ind].index(letter)

    @staticmethod
    def get_letter_dir_dist(letter1, letter2):
        return LayoutUtils.get_letter_pos(letter1) - LayoutUtils.get_letter_pos(letter2)

    @staticmethod 
    def get_letter_dist(letter1, letter2):
        return abs(LayoutUtils.get_letter_dir_dist(letter1, letter2))

    @staticmethod 
    def get_moved_matching_letter(letter, offset):
        row_ind = LayoutUtils.get_letter_row_index(letter)
        pos = LayoutUtils.get_letter_pos(letter)
        moved_row_ind = row_ind + offset
        if moved_row_ind >= len(LayoutUtils.LETTER_ROWS) or moved_row_ind < 0:
            raise Exception("No matching row found")
        if pos >= len(LayoutUtils.LETTER_ROWS[moved_row_ind]):
            return None
        return LayoutUtils.LETTER_ROWS[moved_row_ind][pos]

    @staticmethod 
    def get_matching_letter_below(letter):
        return LayoutUtils.get_moved_matching_letter(letter, 1)

    @staticmethod 
    def get_matching_letter_above(letter):
        return LayoutUtils.get_moved_matching_letter(letter, -1)

    


