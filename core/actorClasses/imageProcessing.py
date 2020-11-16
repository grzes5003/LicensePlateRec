import random
import time
from abc import ABC, abstractmethod

from core.dataClasses.frame import Frame


class ImageProcessingInt(ABC):
    @abstractmethod
    def process(self, _observer, _scheduler):
        pass


class ImageProcessing(ImageProcessingInt):
    def process(self, _observer, _scheduler):
        pass


class ImageProcessingMock(ImageProcessingInt):
    def __init__(self):
        self._limit = 120

    def process(self, _observer, _scheduler):
        for i in range(self._limit):
            time.sleep(random.uniform(0.01, 0.05))
            _observer.on_next(Frame(i))
        _observer.on_completed()
