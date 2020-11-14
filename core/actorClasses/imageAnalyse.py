import random
import time
from abc import abstractmethod, ABC


class ImageAnalyseInt(ABC):
    @staticmethod
    @abstractmethod
    def analyse(_id, frame, queue):
        pass


class ImageAnalyse(ImageAnalyseInt):
    @staticmethod
    def analyse(_id, frame, queue):
        pass


class ImageAnalyseMock(ImageAnalyseInt):
    @staticmethod
    def analyse(_id, frame, queue):
        time.sleep(random.uniform(0.2, 0.055))
        queue.put(frame)
        queue.task_done()
        return frame
