from PIL import ImageDraw
import random

class NoiseGenerator:
    def __init__(self, image):
        self.image = image

    def add_noise(self, min_color, max_color):
        noise_color = random.choice(range(min_color, max_color + 1))
        cx = random.choice(range(self.image.size[0] + 1))
        cy = random.choice(range(self.image.size[1] + 1))
        rx = random.choice(range(1, 8))
        ry = random.choice(range(1, 8))
        ImageDraw.Draw(self.image).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), noise_color)

    def add_noises(self, min_color, max_color, noise_count):
        for i in range(noise_count):
            self.add_noise(min_color, max_color)
