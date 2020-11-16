import random
import time
from abc import abstractmethod, ABC


class ImageAnalyseInt(ABC):
    @staticmethod
    @abstractmethod
    def analyse(_id, frame):
        pass


class ImageAnalyse(ImageAnalyseInt):
    @staticmethod
    def analyse(_id, frame):
        pass


class ImageAnalyseMock(ImageAnalyseInt):
    @staticmethod
    def analyse(_id, frame):
        time.sleep(random.uniform(0.2, 0.055))
        return frame
