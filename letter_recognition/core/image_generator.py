import random
import cv2
import imutils
import math
from PIL import ImageFont, ImageDraw, ImageOps, Image  
import numpy as np
from . import ImageParamsGenerator
from . import NoiseGenerator
from . import ShapeGenerator

class ImageGenerator:
    IMAGE_SIZE = 32
    ROTATE_OFFSET = 8
    NOISE_OFFSET = 40
    ANGLE_BUCKET_SIZE = 10
    
    def __init__(self, max_color_diff, rotate_text=False, empty_text=False):
        self.params_generator = ImageParamsGenerator(max_color_diff, rotate_text, empty_text)
            
    def get_draw_position(self, params):
        text_size = params.font.getsize(params.text)
        offset = params.font.getoffset('TEXT')        
        pos_x = (self.IMAGE_SIZE * 3 - text_size[0] - offset[0]) / 2
        pos_y = (self.IMAGE_SIZE * 3 - text_size[1] - offset[1]) / 2        
        return (pos_x, pos_y)
    
    def get_paste_position(self, rotate_pos):
        pos_x = rotate_pos[0] - self.ROTATE_OFFSET
        pos_y = rotate_pos[1] - self.ROTATE_OFFSET
        return (pos_x, pos_y)
    
    def get_crop_coordinates(self):
        from_pos = self.IMAGE_SIZE - self.ROTATE_OFFSET
        to_pos = 2 * self.IMAGE_SIZE + self.ROTATE_OFFSET
        return (from_pos, from_pos, to_pos, to_pos)
    
    def get_noisy_image(self, params, image_size):
        image = Image.new('L', image_size, params.background)        
        noise_generator = NoiseGenerator(image)
        min_color = params.background - self.NOISE_OFFSET
        max_color = params.background   
        noise_generator.add_noises(min_color, max_color, params.noise_count)
        return image
    
    def get_text_image(self, params):
        rotate_image = self.get_noisy_image(params, (self.IMAGE_SIZE * 3, self.IMAGE_SIZE * 3)) 
        text_image = self.get_noisy_image(params, (self.IMAGE_SIZE, self.IMAGE_SIZE)) 
        draw_pos = self.get_draw_position(params)
        ImageDraw.Draw(rotate_image).text(draw_pos, params.text, params.color, params.font)
        rotate_image = rotate_image.rotate(params.angle)
        rotate_image = rotate_image.crop(self.get_crop_coordinates())
        text_image.paste(rotate_image, self.get_paste_position(params.pos))
        return np.array(text_image, dtype=np.uint8)  

    def get_plain_image(self, params):
        if params.text == ' ':
            image = Image.new('L', (self.IMAGE_SIZE, self.IMAGE_SIZE), params.background)
            NoiseGenerator(image).add_noises(0, 255, params.noise_count)
            ShapeGenerator(image).generate_shape()
            return np.array(image, dtype=np.uint8)
        else:
            return self.get_text_image(params)
        
    def get_gaussian_blur_variation(self, scale):
        if scale <= 0.4:
            return 0.5
        elif scale <= 0.6:
            return 1.5
        else: 
            return 2.5
            
    def get_gaussian_blur_size(self, scale):
        if scale <= 0.4:
            return random.choice([0, 1, 3])
        elif scale <= 0.5:
            return random.choice([0, 1, 3, 5])
        elif scale <= 0.6:
            return random.choice([1, 3, 5, 7])
        elif scale <= 0.75:
            return random.choice([1, 3, 5, 7])
        elif scale <= 0.9:
            return random.choice([1, 5, 9, 13])
        else:
            return random.choice([5, 9, 13, 17])

    def get_uniform_blur_size(self, scale):
        if scale <= 0.4:
            return random.choice([0, 1])
        elif scale <= 0.5:
            return random.choice([0, 1, 2, 3])
        elif scale <= 0.6:
            return random.choice([1, 2, 3, 4])
        elif scale <= 0.75:
            return random.choice([2, 3, 4, 5])
        elif scale <= 0.9:
            return random.choice([3, 4, 5, 6])
        else:
            return random.choice([4, 5, 6, 7])

    def scale_text_blur(self, blur, text):
        if text in ['1', 'I', '{', '}', '(', ')', '[', ']', '$']:
            return blur / 3
        else:
            return blur
        
    def generate_blur_size(self, text, scale, is_gaussian_blur):
        if is_gaussian_blur:
            blur = self.scale_text_blur(self.get_gaussian_blur_size(scale), text)
            return (blur if blur % 2 == 1 else blur + 1)
        else:
            return self.scale_text_blur(self.get_uniform_blur_size(scale), text)
            
    def get_blurred_image(self, image, params):
        is_gaussian_blur = random.choice([False, True])
        blur_x = self.generate_blur_size(params.text, params.scale, is_gaussian_blur)
        blur_y = self.generate_blur_size(params.text, params.scale, is_gaussian_blur)
        if blur_x == 0 or blur_y == 0:
            return image
        if is_gaussian_blur:      
            blur_var = self.get_gaussian_blur_variation(params.scale)
            return cv2.GaussianBlur(image, (blur_x, blur_y), blur_var)
        else:            
            return cv2.blur(image, (blur_x, blur_y))
                
    def get_coloured_image(self, image):
        if random.choice([False, True]):
            return cv2.bitwise_not(image)
        return image
            
    def generate_image(self):
        params = self.params_generator.generate_image_params()
        image = self.get_plain_image(params)
        image = self.get_blurred_image(image, params)
        angle_bucket = int(math.floor(params.angle / ImageGenerator.ANGLE_BUCKET_SIZE))
        return ((params.text, angle_bucket), self.get_coloured_image(image))
