import random
import time
from core.dataClasses.frame import Frame
from core.dataClasses.signal import Signal


class ImageProcessing:
    def __init__(self, processing_queue, management_queue):
        self._limit = 120
        self._processing_queue = processing_queue
        self._management_queue = management_queue

    def process(self):
        for i in range(self._limit):
            # yield i
            time.sleep(random.uniform(0.01, 0.05))
            self._processing_queue.put(Frame(i))
        self._processing_queue.put(None)
        self._management_queue.put(Signal.IMG_PROCESSING_FINISHED)
