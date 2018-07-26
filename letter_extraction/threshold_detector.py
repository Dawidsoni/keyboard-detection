import cv2
from matplotlib import pyplot as plt
from . import ThresholdParams, ThresholdExtractor, ImageFragmentExtractor, ImageFragmentFilter, FragmentShaper

class ThresholdDetector:
    DEFAULT_DET_PARAMS = ThresholdParams(30, -30, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE, 3)
    MIN_FRAGMENT_SCALE = 100
    MAX_FRAGMENT_SCALE = 10
    FRAGMENT_SCALE = 1.1

    def __init__(self, det_params=None):
        if det_params is None:
            det_params = ThresholdDetector.DEFAULT_DET_PARAMS
        self.det_params = det_params

    @staticmethod
    def get_min_fragment_size(image):
        return int(max(image.shape[0], image.shape[1]) / ThresholdDetector.MIN_FRAGMENT_SCALE)

    @staticmethod
    def get_max_fragment_size(image):
        return int(max(image.shape[0], image.shape[1]) / ThresholdDetector.MAX_FRAGMENT_SCALE)

    def get_fragment_list(self, image):
        min_fragment_size = ThresholdDetector.get_min_fragment_size(image)
        max_fragment_size = ThresholdDetector.get_max_fragment_size(image)    
        contours_detector = ThresholdExtractor(self.det_params)
        contour_list = contours_detector.get_contours(image)
        fragment_extractor = ImageFragmentExtractor(image, ThresholdDetector.FRAGMENT_SCALE)  
        image_fragment_filter = ImageFragmentFilter(min_fragment_size, max_fragment_size)    
        fragment_shaper = FragmentShaper()
        fragment_list = map(fragment_extractor.extract_image_fragment, contour_list)
        fragment_list = image_fragment_filter.filter_fragments(fragment_list)
        fragment_list = map(fragment_shaper.shape_fragment, fragment_list)
        return fragment_list
