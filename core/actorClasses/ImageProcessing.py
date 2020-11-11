import random
import time


class ImageProcessing:
    def __init__(self):
        self._limit = 100

    def process(self):
        for i in range(self._limit):
            yield i
            time.sleep(random.uniform(0.01, 0.1))
