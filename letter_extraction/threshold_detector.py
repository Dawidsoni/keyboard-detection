import cv2
import numpy as np
from matplotlib import pyplot as plt
from collections import namedtuple

thres_params_names = ['block_scale', 'sub_threshold', 'retr_type', 'retr_approx', 'min_poly']
ThresholdParams = namedtuple('ThresholdParams', thres_params_names)

class ThresholdDetector:
    DEFAULT_DET_PARAMS = ThresholdParams(30, -30, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE, 3)

    def __init__(self, det_params=None):
        if det_params is None:
            det_params = ThresholdDetector.DEFAULT_DET_PARAMS
        self.det_params = det_params        
        
    def create_threshold_image(self, image, reverse_color=False):   
        if reverse_color:
            image = cv2.bitwise_not(image)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        block_size = int(max(image.shape[0], image.shape[1]) / self.det_params.block_scale)
        if block_size % 2 == 0:
            block_size += 1
        thresh_type = cv2.ADAPTIVE_THRESH_MEAN_C
        sub_thres = self.det_params.sub_threshold
        return cv2.adaptiveThreshold(gray_image, 255, thresh_type, cv2.THRESH_BINARY, block_size, sub_thres)       
        
    def is_contour_valid(self, contour):
        poly_tolerance = 0.01 * cv2.arcLength(contour, True)
        poly_approx = cv2.approxPolyDP(contour, poly_tolerance, True)
        return (len(poly_approx) > self.det_params.min_poly)
        
    def get_white_contours(self, image, reverse_color=False):
        threshold = self.create_threshold_image(image, reverse_color)
        retr_type, retr_approx = self.det_params.retr_type, self.det_params.retr_approx        
        contours, _ = cv2.findContours(threshold, retr_type, retr_approx)
        return filter(self.is_contour_valid, contours)        
        
    def get_contours(self, image):
        return self.get_white_contours(image, False) + self.get_white_contours(image, True)
    
    def create_contours_image(self, image, reverse_color=False):
        contours_list = self.get_white_contours(image, reverse_color)
        contours_image = image.copy()        
        for cnt in contours_list:
            contour_color = np.random.randint(255, size=3)
            cv2.drawContours(contours_image, [cnt], 0, contour_color, -1)   
        return contours_image
    
    def plot_internal_image(self, image, cmap=None):
        plt.figure(figsize=(14, 9))        
        plt.imshow(image, cmap=cmap)
        plt.show()        
    
    def plot_contours_images(self, image):
        self.plot_internal_image(image)
        self.plot_internal_image(self.create_threshold_image(image, False), 'gray')
        self.plot_internal_image(self.create_contours_image(image, False))        
        self.plot_internal_image(self.create_threshold_image(image, True), 'gray')
        self.plot_internal_image(self.create_contours_image(image, True))
        
