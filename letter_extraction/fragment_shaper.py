import cv2

class FragmentShaper:
    def __init__(self, fragment_size=(32, 32)):
        self.fragment_size = fragment_size

    def resize_fragment(self, fragment):
        return (fragment[0], cv2.resize(fragment[1], self.fragment_size))

    def gray_fragment(self, fragment):
        return (fragment[0], cv2.cvtColor(fragment[1], cv2.COLOR_RGB2GRAY))

    def shape_fragment(self, fragment):
        return self.resize_fragment(self.gray_fragment(fragment))
