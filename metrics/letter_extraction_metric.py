from . import KeyboardLayout

class LetterExtractionMetric:
    @staticmethod
    def _get_detected_letters(layout, fragment_extractor):
        fragment_list = fragment_extractor.get_fragment_list(layout.get_image())
        letter_coords = map(lambda x: x[0], fragment_list)
        return map(lambda x: layout.find_letter(x['start_pos'], x['end_pos']), letter_coords)

    @staticmethod
    def _get_coefficient_of_coverage(detected_letters):
        return len(filter(lambda x: x is not None, detected_letters)) / float(len(detected_letters))

    @staticmethod
    def _get_all_letters_coverage(detected_letters):
        total_coverage = 0
        layout_chars = KeyboardLayout.get_layout_chars()
        for layout_char in layout_chars:
            total_coverage += any([x == layout_char for x in detected_letters])
        return total_coverage / float(len(layout_chars))
    
    @staticmethod
    def _get_average_letters_coverage(detected_letters):
        total_coverage = 0
        layout_chars = KeyboardLayout.get_layout_chars()
        for layout_char in layout_chars:
            total_coverage += len(filter(lambda x: x == layout_char, detected_letters))
        return total_coverage / float(len(layout_chars))

    @staticmethod
    def get_rating(layout, fragment_extractor):
        detected_letters = LetterExtractionMetric._get_detected_letters(layout, fragment_extractor)
        coef_coverage = LetterExtractionMetric._get_coefficient_of_coverage(detected_letters)
        all_lett_coverage = LetterExtractionMetric._get_all_letters_coverage(detected_letters)
        av_lett_coverage = LetterExtractionMetric._get_average_letters_coverage(detected_letters)
        score = all_lett_coverage * 50 + coef_coverage * 50
        return {
            'coef_coverage': coef_coverage,
            'all_lett_coverage': all_lett_coverage,
            'av_lett_coverage': av_lett_coverage,
            'score': score
        }

    @staticmethod
    def test_layouts(layouts, fragment_extractor):
        total_score = 0
        for layout in layouts:
            rating = LetterExtractionMetric.get_rating(layout, fragment_extractor)
            total_score += rating['score']
            print("{}: {}".format(layout.layout_name, rating))
        print("Total score: {}".format(total_score))

    @staticmethod
    def score_layouts(layouts, fragment_extractor):
        return sum(map(lambda x: LetterExtractionMetric.get_rating(x, fragment_extractor)['score'], layouts))

    @staticmethod
    def test_grouped_layouts(layouts, fragment_extractor):
        stable_layouts = filter(lambda x: x.is_stable_layout(), layouts)
        rotated_layouts = filter(lambda x: x.is_rotated_layout(), layouts)
        print("Stable layouts:")
        LetterExtractionMetric.test_layouts(stable_layouts, fragment_extractor)
        print("Rotated layouts:")
        LetterExtractionMetric.test_layouts(rotated_layouts, fragment_extractor)

        
