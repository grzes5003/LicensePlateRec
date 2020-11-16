import random
import time
from abc import abstractmethod, ABC

from core.dataClasses.LicensePlate import LicensePlate
from core.dataClasses.frame import Frame


class ImageAnalyseInt(ABC):
    @staticmethod
    @abstractmethod
    def analyse(_id, frame: Frame) -> LicensePlate:
        pass


class ImageAnalyse(ImageAnalyseInt):
    @staticmethod
    def analyse(_id, frame: Frame) -> LicensePlate:
        pass


class ImageAnalyseMock(ImageAnalyseInt):
    @staticmethod
    def analyse(_id, frame: Frame) -> LicensePlate:
        time.sleep(random.uniform(0.01, 0.05))
        return LicensePlate(id_=frame.id_)
