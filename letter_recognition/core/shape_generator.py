from PIL import Image, ImageDraw
import random
import numpy as np

class ShapeGenerator:
    def __init__(self, image):
        self.image = image
        self.im_draw = ImageDraw.Draw(image)

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
            pos_outx, pos_outy = random.randint(-24, -8), random.randint(-24, -8) 
            return [(pos_outx, pos_outy), (pos_inx, pos_iny)]
        elif circle_type == 2:
            pos_outx, pos_outy = random.randint(-24, -8), random.randint(40, 56)
            return [(pos_outx, pos_iny), (pos_inx, pos_outy)]
        elif circle_type == 3:
            pos_outx, pos_outy = random.randint(40, 56), random.randint(-24, -8)
            return [(pos_inx, pos_outy), (pos_outx, pos_iny)]
        elif circle_type == 4:
            pos_outx, pos_outy = random.randint(40, 56), random.randint(40, 56)
            return [(pos_inx, pos_iny), (pos_outx, pos_outy)]
        else: 
            raise ValueError("Invalid circle type")

    def generate_lines(self):
        for i in range(random.randint(1, 4)):
            pos = self.generate_line_position()
            color = random.randint(0, 255)
            width = random.randint(2, 10)
            self.im_draw.line(pos, color, width)

    def generate_circles(self):
        for i in range(random.randint(1, 3)):
            pos = self.generate_polygon_position()
            color = random.randint(0, 255)
            self.im_draw.ellipse(pos, color)

    def generate_rectangles(self):
        for i in range(random.randint(1, 4)):
            pos = self.generate_polygon_position()
            color = random.randint(0, 255)
            self.im_draw.rectangle(pos, color)

    def generate_shape(self):
        shape_count = np.random.choice(4, replace=False, p=[0.2, 0.6, 0.1, 0.1])
        shape_types = np.random.choice(3, shape_count, replace=False)
        for shape_type in shape_types:
            if shape_type == 0:
                self.generate_lines()
            elif shape_type == 1:
                self.generate_circles()
            elif shape_type == 2:
                self.generate_rectangles()
            else:
                raise ValueError("Invalid shape type")
