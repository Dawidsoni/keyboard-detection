import sys
sys.path.append('..')
from letter_extraction import ThresholdParams, EdgeParams, ThresholdDetector, EdgeDetector, ChunkExtractor
from letter_extraction import ExtractFragmentParams, ContoursExtractor, CompositeExtractor
from metrics import KeyboardLayout, LetterExtractionMetric

layout_func = (lambda x: KeyboardLayout("../keyboards/layouts/keyboard{}.layout".format(x), '../'))
layouts = map(layout_func, range(1, 26))
comp_detector = CompositeExtractor([ContoursExtractor(EdgeDetector()), ContoursExtractor(ThresholdDetector())])
extract_params = ExtractFragmentParams(150, 20, 1.6)
edge_detector = ContoursExtractor(EdgeDetector(), extract_params)
LetterExtractionMetric.test_layouts(layouts, edge_detector)
