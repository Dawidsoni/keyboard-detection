import sys
sys.path.append('..')
from letter_extraction import ThresholdParams, EdgeParams, ThresholdDetector, EdgeDetector, ChunkExtractor
from letter_extraction import ExtractFragmentParams, ContoursExtractor, CompositeExtractor
from metrics import KeyboardLayout, LetterExtractionMetric

layout_func = (lambda x: KeyboardLayout("../keyboards/layouts/keyboard{}.layout".format(x), '../'))
layouts = map(layout_func, range(1, 26))
thres_detector = CompositeExtractor([ContoursExtractor(EdgeDetector()), ContoursExtractor(ThresholdDetector())])
LetterExtractionMetric.test_layouts(layouts, thres_detector)
