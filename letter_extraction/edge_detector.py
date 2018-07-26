import cv2
from . import EdgeExtractor, EdgeParams, ImageFragmentFilter, ImageFragmentExtractor, FragmentShaper

class EdgeDetector:
    DEFAULT_DET_PARAMS = EdgeParams(75, 200, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE, 10, 1000)
    FRAGMENT_SCALE = 2.5

    def __init__(self, det_params=None):
        if det_params is None:
            det_params = EdgeDetector.DEFAULT_DET_PARAMS
        self.det_params = det_params

    def get_fragment_list(self, image):
        contours_detector = EdgeExtractor(self.det_params)
        contour_list = contours_detector.get_contours(image)
        fragment_extractor = ImageFragmentExtractor(image, EdgeDetector.FRAGMENT_SCALE)  
        max_fragment_size = min(image.shape[0], image.shape[1])
        image_fragment_filter = ImageFragmentFilter(0, max_fragment_size)    
        fragment_shaper = FragmentShaper()
        fragment_list = map(fragment_extractor.extract_image_fragment, contour_list)
        fragment_list = image_fragment_filter.filter_fragments(fragment_list)
        fragment_list = map(fragment_shaper.shape_fragment, fragment_list)
        return fragment_list

