from PIL import ImageFont
import os

class FontProxy:
    def __init__(self):
        self.font_dict = {}
        self.init_font_names()

    def init_font_names(self):
        self.font_names = filter(lambda x: ".ttf" in x, os.listdir('fonts/'))
        self.font_names = map(lambda x: x[:-4], self.font_names)

    def get_font_names(self):
        return self.font_names
        
    def generate_font(self, font_name, font_size):
        if font_name not in self.get_font_names():
            raise Exception("Invalid font name")
        font_key = (font_name, font_size)
        if font_key not in self.font_dict:
            font_path = "fonts/{0}.ttf".format(font_name)
            self.font_dict[font_key] = ImageFont.truetype(font_path, font_size)
        return self.font_dict[font_key]
