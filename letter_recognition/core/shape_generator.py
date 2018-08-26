from PIL import Image, ImageDraw
import random
import numpy as np

class ShapeGenerator:
    COLOR_OFFSET = 30

    def __init__(self, image, text_color=None):
        self.image = image
        self.im_draw = ImageDraw.Draw(image)
        self.text_color = text_color

    def generate_color(self):
        if self.text_color is None:
            return random.randint(0, 255)
        color_type = random.randint(0, 1)
        if color_type == 0 and self.text_color >= 128:
            return 0
        elif color_type == 0 and self.text_color < 128:
            return 255
        else:
            min_color = max(0, self.text_color - self.COLOR_OFFSET)
            max_color = min(255, self.text_color + self.COLOR_OFFSET)
            return random.randint(min_color, max_color)

    def generate_line_position(self):
        line_type = random.randint(1, 4)
        if line_type == 1:
            pos = random.randint(2, 31)
            return [(-1, pos), (33, pos)]
        elif line_type == 2:
            pos = random.randint(2, 31)
            return [(pos, -1), (33, pos)]
        elif line_type == 3:
            pos1, pos2 = random.randint(2, 31), random.randint(2, 31)
            return [(-1, pos1), (33, pos2)] 
        elif line_type == 4:
            pos1, pos2 = random.randint(2, 31), random.randint(2, 31)
            return [(pos1, -1), (pos2, 33)] 
        else:
            raise ValueError("Invalid line type")

    def generate_polygon_position(self):
        circle_type = random.randint(1, 4)
        pos_inx, pos_iny = random.randint(8, 24), random.randint(8, 24)
        if circle_type == 1:
            pos_outx, pos_outy = random.randint(-24, 0), random.randint(-24, 0) 
            return [(pos_outx, pos_outy), (pos_inx, pos_iny)]
        elif circle_type == 2:
            pos_outx, pos_outy = random.randint(-24, 0), random.randint(32, 56)
            return [(pos_outx, pos_iny), (pos_inx, pos_outy)]
        elif circle_type == 3:
            pos_outx, pos_outy = random.randint(32, 56), random.randint(-24, 0)
            return [(pos_inx, pos_outy), (pos_outx, pos_iny)]
        elif circle_type == 4:
            pos_outx, pos_outy = random.randint(32, 56), random.randint(32, 56)
            return [(pos_inx, pos_iny), (pos_outx, pos_outy)]
        else: 
            raise ValueError("Invalid circle type")

    def generate_lines(self):
        for i in range(random.randint(1, 10)):
            pos = self.generate_line_position()
            color = self.generate_color()
            width = random.randint(2, 5)
            self.im_draw.line(pos, color, width)

    def generate_circles(self):
        for i in range(random.randint(1, 10)):
            pos = self.generate_polygon_position()
            color = self.generate_color()
            self.im_draw.ellipse(pos, color)

    def generate_rectangles(self):
        for i in range(random.randint(1, 10)):
            pos = self.generate_polygon_position()
            color = self.generate_color()
            self.im_draw.rectangle(pos, color)

    def generate_box(self):
        color = self.generate_color()
        border_size = random.randint(1, 5)
        self.im_draw.rectangle((0, 0, 32, border_size), color)
        self.im_draw.rectangle((0, 0, border_size, 32), color)
        self.im_draw.rectangle((32 - border_size, 32, 32, 32), color)
        self.im_draw.rectangle((32, 32 - border_size, 32, 32), color)

    def generate_shape(self):
        shape_count = np.random.choice(4, p=[0.2, 0.6, 0.1, 0.1], replace=False)
        shape_types = sorted(np.random.choice(4, shape_count, replace=False))
        for shape_type in shape_types:
            if shape_type == 0:
                self.generate_rectangles()
            elif shape_type == 1:
                self.generate_circles()
            elif shape_type == 2:
                self.generate_lines()
            elif shape_type == 3:
                self.generate_box()
            else:
                raise ValueError("Invalid shape type")
