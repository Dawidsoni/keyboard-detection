class CompositeExtractor:
    def __init__(self, base_extractors):
        self.base_extractors = base_extractors

    def get_fragment_list(self, image):
        fragment_list = []
        for extractor in self.base_extractors:
            fragment_list += extractor.get_fragment_list(image)
        return fragment_list

