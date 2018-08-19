import random
import string
from collections import namedtuple
import numpy as np
from . import FontProxy

params_list = ['pos', 'scale', 'is_empty', 'text', 'font', 'background', 'color', 'angle', 'noise_count']
ImageParamsTuple = namedtuple('ImageParams', params_list)

class ImageParamsGenerator:        
    DEFAULT_FONT_SIZE = 40
    MIN_FONT_SCALE = 0.275

    def __init__(self, max_color_diff, rotate_text=False, empty_text=False):
        self.max_color_diff = max_color_diff
        self.rotate_text = rotate_text
        self.empty_text = empty_text
        self.font_proxy = FontProxy()

    def generate_is_empty(self):
        return (random.randint(1, 30) == 1)

    def generate_empty_text(self):
        if random.choice([False, True]):
            return ' '
        return random.choice([
            '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '[', ']', 
            '{', '}', '"', ';', ':', '?', '<', '>', '~', 'b', 'e', 'p', 'Alt',
            'Ctrl', 'Esc', 'Enter', 'End', 'Home', 'Delete', 'Num', 'Page', 'Up', 
            'Down', 'Ins', 'Lock', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 
            'F9', 'F10', 'F11', 'F12', 'Tab', 'Caps', 'Shift', 'Scroll', 'Print'
        ])

    def generate_non_empty_text(self):
        char_list = list(string.ascii_uppercase + string.digits)
        return random.choice(char_list)

    def generate_text(self, is_empty):
        if is_empty:
            return self.generate_empty_text()
        else:
            return self.generate_non_empty_text()

    def generate_scale(self, text):
        if len(text) >= 4:
            return self.MIN_FONT_SCALE
        elif len(text) == 3:
            return random.uniform(self.MIN_FONT_SCALE, 0.4)
        elif len(text) == 2:
            return random.uniform(self.MIN_FONT_SCALE, 0.6)
        elif text in ['I', 'J']: 
            return random.uniform(self.MIN_FONT_SCALE, 0.85)        
        elif text in ['W', 'M', 'Q', '1']:
            return random.uniform(self.MIN_FONT_SCALE, 0.9)
        elif text in ['~', '!', ':', ';', '"', '&']:
            return random.uniform(0.7, 1.0)
        elif text in ['(', ')', '[', ']', '{', '}', '$']:
            return random.uniform(0.4, 0.7)
        else:
            return random.uniform(self.MIN_FONT_SCALE, 1.0)

    def generate_position(self, scale):
        max_pos = int(8 - ((scale - 0.275) / 0.675) * 8)
        pos_x = random.choice(range(-max_pos, max_pos + 1))
        pos_y = random.choice(range(-max_pos, max_pos + 1))   
        return (pos_x, pos_y)

    def get_forbidden_fonts(self, text):
        if text == '1':
            return ['CenturyGothicBoldItalic', 'CenturyGothicBold', 'CenturyGothicItalic', 'CenturyGothic',
            'KGNoRegrets', 'TimesNewRomanBold', 'FuturaBookItalic', 'FuturaBook', 'TimesNewRomanItalic',
            'ArialRounded', 'KGLifeisMessy', 'DK Cool Crayon', 'KGBrokenVesselsSketch']
        elif text == '0':
            return ['SansSerifBold', 'VeraSeBd', 'ArialRounded', 'VeraSe', 'SansSerifBoldItalic', 'ArialRoundedLight',
            'Arial', 'AndaleMonoBold', 'CenturyGothic', 'HelveticaBlackOblique', 'KGNoRegrets', 'ArialRoundedExtraBold', 
            'SansSerifItalic', 'FuturaBookItalic', 'ArialRoundedBold', 'FuturaBook', 'KGLifeisMessy', 'DK Cool Crayon', 
            'KGBrokenVesselsSketch']
        elif text == 'O':
            return ['SansSerif', 'HelveticaCondensedLightOblique', 'HelveticaCondensedLight', 'AndaleMono', 
            'AndaleMonoBold']
        elif text in ['(', ')', '[', ']', '{', '}', '%', '$']:
            return ['TimesNewRomanBoldItalic', 'VeraSeBd', 'ArialRounded', 'HelveticaCondensedLightOblique', 
            'DK Cool Crayon', 'KGBrokenVesselsSketch', 'TimesNewRomanBold', 'HelveticaBlackOblique', 'KGLifeisMessy',
            'CenturyGothicBoldItalic', 'ArialRounded', 'CenturyGothicBold']
        else:
            return []

    def generate_font(self, text, scale):
        all_fonts = self.font_proxy.get_font_names()
        forbidden_fonts = self.get_forbidden_fonts(text)
        font_list = filter(lambda x: x not in forbidden_fonts, all_fonts)
        font_name = random.choice(font_list)
        font_size = int(self.DEFAULT_FONT_SIZE * scale)
        return self.font_proxy.generate_font(font_name, font_size)
            
    def generate_image_text_colors(self):
        image_color = random.choice(range(0, 256 - self.max_color_diff))
        text_color = random.choice(range(image_color + self.max_color_diff, 256))
        return (image_color, text_color)
    
    def generate_rotation_angle(self, text):
        if self.rotate_text == False:
            return 0
        if text in ['6', '9', 'W', 'M']:
            return random.choice(range(0, 45) + range(315, 359))
        return random.choice(range(0, 359))
    
    def generate_noise_count(self, text):
        if text == ' ':
            return random.choice([0, 3, 20, 50])
        return random.choice(np.linspace(50, 200, 11, dtype=np.int32))
    
    def generate_image_params(self):    
        is_empty = self.generate_is_empty()
        text = self.generate_text(is_empty)
        scale = self.generate_scale(text)        
        pos = self.generate_position(scale)
        font = self.generate_font(text, scale)
        background, color = self.generate_image_text_colors()
        angle = self.generate_rotation_angle(text)
        noise_count = self.generate_noise_count(text)
        return ImageParamsTuple(pos, scale, is_empty, text, font, background, color, angle, noise_count)
