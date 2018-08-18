import sys
import cv2
sys.path.append('..')
from letter_extraction import ThresholdParams, EdgeParams, ThresholdDetector, EdgeDetector, ChunkExtractor
from letter_extraction import ExtractFragmentParams, ContoursExtractor, CompositeExtractor
from metrics import KeyboardLayout, LetterExtractionMetric

layout_func = (lambda x: KeyboardLayout("../keyboards/layouts/keyboard{}.layout".format(x), '../'))
layouts = map(layout_func, range(1, 26))
comp_detector = CompositeExtractor([ContoursExtractor(EdgeDetector()), ContoursExtractor(ThresholdDetector())])
edge_params = EdgeParams(min_edge_thres=50, max_edge_thres=230, retr_type=1L, retr_approx=2L, min_poly=3, max_area_scale=1)
extract_params = ExtractFragmentParams(min_scale=100, max_scale=30, extract_scale=1.8)
thres_detector = ContoursExtractor(ThresholdDetector())
edge_detector = ContoursExtractor(EdgeDetector(edge_params), extract_params)
LetterExtractionMetric.test_layouts(layouts, edge_detector)
