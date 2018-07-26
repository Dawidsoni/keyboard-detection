import cv2
from matplotlib import pyplot as plt
import numpy as np
from collections import namedtuple

edge_params_names = ['min_edge_thres', 'max_edge_thres', 'retr_type', 'retr_approx', 'min_poly', 'max_area']
EdgeParams = namedtuple('EdgeParams', edge_params_names)

class EdgeExtractor:
    def __init__(self, det_params):
        self.det_params = det_params        
        
    def create_edged_image(self, image):
        min_thres = self.det_params.min_edge_thres
        max_thres = self.det_params.max_edge_thres
        return cv2.Canny(image, min_thres, max_thres)
        
    def is_contour_valid(self, contour):
        if cv2.contourArea(contour) > self.det_params.max_area:
            return False
        if len(contour) > self.det_params.max_area:
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
        return filter(self.is_contour_valid, contours)
    
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
