import cv2

class ImageFragmentExtractor:
    def __init__(self, image, fragment_scale):
        self.image = image
        self.fragment_scale = fragment_scale
        
    def get_scaled_size(self, start_point, end_point):
        center_point = (start_point + end_point) / 2.0
        start_scaled = center_point - self.fragment_scale * (center_point - start_point)
        end_scaled = center_point + self.fragment_scale * (end_point - center_point)
        return int(start_scaled), int(end_scaled)
    
    def extract_image_fragment(self, contour):
        start_x, start_y, width, height = cv2.boundingRect(contour)
        width, height = max(width, height), max(width, height)
        start_x, end_x = self.get_scaled_size(start_x, start_x + width)
        start_y, end_y = self.get_scaled_size(start_y, start_y + height)
        fragment_pos = {'start_pos': (start_x, start_y), 'end_pos': (end_x, end_y)}
        return (fragment_pos, self.image[start_y:end_y, start_x:end_x, :])
