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
    for min_scale in [100, 200]:
        for max_scale in [20, 10]:
            for extract_scale in [0.8, 0.9, 1.0, 1.1, 1.15, 1.2, 1.25, 1.3, 1.4, 1.5]:
                try:
                    extract_params = ExtractFragmentParams(min_scale, max_scale, extract_scale)
                    score = test_contours_extractor(contours_detector, extract_params)
                    if score > max_score:
                        max_score = score
                        best_params = extract_params
                except:
                    pass
    return {'score': max_score, 'params': best_params}

def log(message=""):
    print(message)
    with open('extraction_params.data', 'a+') as f_stream:
        f_stream.write(message + '\n')

def test_edge_detector_params():
    max_score = 0.0
    best_params = None
    for r_approx in [cv2.CHAIN_APPROX_SIMPLE, cv2.CHAIN_APPROX_TC89_L1]:
        for r_type in [cv2.RETR_LIST, cv2.RETR_TREE, cv2.RETR_EXTERNAL]:
            for min_thres in [50, 75, 100]:
                for max_thres in [170, 200, 230]:
                    for min_poly in [3, 5]:
                        edge_params = EdgeParams(min_thres, max_thres, r_type, r_approx, min_poly, 1)
                        edge_detector = EdgeDetector(edge_params)
                        score = test_extract_params(edge_detector)['score']
                        if score > max_score:
                            max_score = score
                            best_params = edge_params
                        log("Params: {}, score: {} (best: {})".format(edge_params, score, max_score))                           
    return best_params

def test_thres_detector_params():
    max_score = 0.0
    best_params = None
    for r_approx in [cv2.CHAIN_APPROX_SIMPLE, cv2.CHAIN_APPROX_TC89_L1]:
        for r_type in [cv2.RETR_LIST, cv2.RETR_TREE, cv2.RETR_EXTERNAL]:
            for min_poly in [3, 5]:
                for b_scale in [20, 30, 40]:
                    for s_thres in [-40, -30, -20]:                                                                        
                        thres_params = ThresholdParams(b_scale, s_thres, r_type, r_approx, min_poly)
                        contours_detector = ThresholdDetector(thres_params)
                        score = test_extract_params(contours_detector)['score']
                        if score > max_score:
                            max_score = score
                            best_params = thres_params
                        log("Params: {}, score: {} (best: {})".format(thres_params, score, max_score))                        
    return best_params


thres_params = test_thres_detector_params()
log(str(thres_params))
log()
edge_params = test_edge_detector_params()
log(str(edge_params))
log()


