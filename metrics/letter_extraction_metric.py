from . import KeyboardLayout

class LetterExtractionMetric:
    def __init__(self, keyboard_layouts):
        self.keyboard_layouts = keyboard_layouts

    def _add_real_letters(self, layout, letter_coords):
        for letter_coord in letter_coords:
            letter_coord['letter'] = layout.find_letter(letter_coord['start_pos'], letter_coord['end_pos'])

    def _test_layouts(self, layouts, extract_func):
        detected_letters = []
        for layout in layouts:
            letter_coords = extract_func(layout['filepath'])
            detected_letters += map(lambda x: layout.find_letter(x['start_pos'], x['end_pos']), letter_coords)
        for layout_char in KeyboardLayout.get_layout_chars():
            char_elements = filter(lambda x: x == layout_char, detected_letters)
            print("Elements for {0}: {1}".format(layout_char, len(char_elements)))
        empty_chars = filter(lambda x: x not in KeyboardLayout.get_layout_chars(), detected_letters)
        print("Letters are {0} of {1} of all detected coords".format(len(empty_chars), len(detected_letters))

    def test_extraction_method(self, extract_func):
        stable_layouts = filter(lambda x: x.is_stable_layout(), self.keyboard_layouts)
        rotated_layouts = filter(lambda x: x.is_rotated_layout(), self.keyboard_layouts)
        print("Stable layouts:")
        self._test_layouts(stable_layouts, extract_func)
        print("Rotated layouts:")
        self._test_layouts(rotated_layouts, extract_func)

        
