import sys
import numpy as np
import cv2
sys.path.append('..')    
from letter_extraction import ThresholdParams, ThresholdDetector, EdgeParams, EdgeDetector, ChunkExtractor
from letter_extraction import ExtractFragmentParams, ContoursExtractor, CompositeExtractor
from metrics import KeyboardLayout, LetterExtractionMetric

layout_func = (lambda x: KeyboardLayout("../keyboards/layouts/keyboard{}.layout".format(x), '../'))
keyboard_layouts = map(layout_func, range(1, 26))

def test_contours_extractor(contours_detector, extract_params):
    contours_extractor = ContoursExtractor(contours_detector, extract_params)
    return LetterExtractionMetric.score_layouts(keyboard_layouts, contours_extractor)

def test_extract_params(contours_detector):
    max_score = 0.0
    best_params = None
    for min_scale in [50, 100, 150, 200]:
        for max_scale in [30, 20, 10, 1]:
            for extract_scale in [1.6, 1.65, 1.7, 1.8]:#[0.7, 0.8, 0.9, 1.0, 1.1, 1.15, 1.2, 1.25, 1.3, 1.4, 1.5, 1.6]:
                try:
                    extract_params = ExtractFragmentParams(min_scale, max_scale, extract_scale)
                    score = test_contours_extractor(contours_detector, extract_params)
                    if score > max_score:
                        max_score = score
                        best_params = extract_params
                except:
                    pass
    return {'score': max_score, 'params': best_params}

thres_params = ThresholdParams(30, -30, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE, 3)
print(test_extract_params(ThresholdDetector(thres_params)))
