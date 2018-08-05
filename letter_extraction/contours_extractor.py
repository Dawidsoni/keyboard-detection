import cv2
from . import ImageFragmentFilter, ImageFragmentExtractor, FragmentShaper, ExtractFragmentParams

class ContoursExtractor:
    DEFAULT_EXTRACT_PARAMS = ExtractFragmentParams(150, 20, 1.6)

    def __init__(self, contours_detector, extract_params=None):
        self.contours_detector = contours_detector
        if extract_params is None:
            extract_params = ContoursExtractor.DEFAULT_EXTRACT_PARAMS
        self.extract_params = extract_params

    def get_fragment_list(self, image):
        contour_list = self.contours_detector.get_contours(image)
        fragment_extractor = ImageFragmentExtractor(image, self.extract_params.extract_scale)  
        image_fragment_filter = ImageFragmentFilter(image, self.extract_params)    
        fragment_shaper = FragmentShaper()
        fragment_list = map(fragment_extractor.extract_image_fragment, contour_list)
        fragment_list = image_fragment_filter.filter_fragments(fragment_list)
        fragment_list = map(fragment_shaper.shape_fragment, fragment_list)
        return fragment_list

