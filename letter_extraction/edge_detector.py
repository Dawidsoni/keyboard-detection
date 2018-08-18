import cv2
from matplotlib import pyplot as plt
import numpy as np
from collections import namedtuple

edge_params_names = ['min_edge_thres', 'max_edge_thres', 'retr_type', 'retr_approx', 'min_poly', 'max_area_scale']
EdgeParams = namedtuple('EdgeParams', edge_params_names)

class EdgeDetector:
    DEFAULT_DET_PARAMS = EdgeParams(50, 170, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE, 3, 1)

    def __init__(self, det_params=None):
        if det_params is None:
            det_params = EdgeDetector.DEFAULT_DET_PARAMS
        self.det_params = det_params        
        
    def create_edged_image(self, image):
        min_thres = self.det_params.min_edge_thres
        max_thres = self.det_params.max_edge_thres
        return cv2.Canny(image, min_thres, max_thres)

    def get_max_area(self, image):
        return int(max(image.shape[0], image.shape[1]) / self.det_params.max_area_scale)
        
    def is_contour_valid(self, image, contour):
        if len(contour) > self.get_max_area(image):
            return False
        return True                
        poly_tolerance = 0.01 * cv2.arcLength(contour, True)
        poly_approx = cv2.approxPolyDP(contour, poly_tolerance, True)
        return (len(poly_approx) > self.det_params.min_poly)
        
    def get_contours(self, image):
        edged_image = self.create_edged_image(image)
        ret, thresh = cv2.threshold(edged_image, 127, 255, 0)        
        retr_type, retr_approx = self.det_params.retr_type, self.det_params.retr_approx
        contours, _ = cv2.findContours(thresh, retr_type, retr_approx)
        return filter(lambda x: self.is_contour_valid(image, x), contours)
    
    def create_contours_image(self, image):
        contours_list = self.get_contours(image)
        contours_image = image.copy()        
        for cnt in contours_list:
            contour_color = np.random.randint(255, size=3)
            cv2.drawContours(contours_image, [cnt], 0, contour_color, -1)   
        return contours_image
    
    def plot_contours_image(self, image):
        edged_image = self.create_edged_image(image)
        plt.figure(figsize=(14, 9))
        plt.imshow(edged_image, cmap='gray')
        plt.show()                
        contours_image = self.create_contours_image(image)
        plt.figure(figsize=(14, 9))
        plt.imshow(contours_image)
        plt.show()
