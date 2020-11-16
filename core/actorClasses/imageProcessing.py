import random
import time
from abc import ABC, abstractmethod

from core.dataClasses.frame import Frame


class ImageProcessingInt(ABC):
    """
    Base Abstract class aka Interface for Image processing class
    """
    @abstractmethod
    def process(self, _observer, _scheduler):
        """
        Imports video clip and samples it.
        Sampled Images are processed and encapsulated into Frame class.
        As a result those are emitted to manager by _observer.on_next()
        :param _observer: rx.core.typing.Observer
        :param _scheduler: rx.core.typing.Scheduler
        :return:
        """
        raise NotImplemented


class ImageProcessing(ImageProcessingInt):
    def process(self, _observer, _scheduler):
        pass


class ImageProcessingMock(ImageProcessingInt):
    def __init__(self):
        self._limit = 120

    def process(self, _observer, _scheduler):
        for i in range(self._limit):
            time.sleep(random.uniform(0.01, 0.05))
            # each time "send" processed image by evoking _observer.on_next( /analysed Frame/ ) method
            _observer.on_next(Frame(i))
        # when process is completed notify Manager by calling _observer.on_completed()
        _observer.on_completed()
