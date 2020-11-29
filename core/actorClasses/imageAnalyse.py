import random
import time
import logging
import sys
from abc import abstractmethod, ABC
from core.dataClasses import LicensePlate
from pathlib import Path

# module files are inside another directory, so python dirs search should be expanded
sys.path.append("alpr")
from lprec import Alpr

PATH_TO_CONF = Path("alpr/config.alpr.conf")
PATH_TO_RUN_TIME = Path("alpr/runtime-data")
COUNTRY = "eu"
REGION = "pl"
from core.dataClasses.LicensePlate import LicensePlate
from core.dataClasses.frame import Frame



def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class MLInstance:
    """
    In order to operate only on one ML instance, thus saving memory in
    multi-threading implementation, singleton class is provided. This way
    all the instances of analyse function will operate on the same ML instance.

    All created instances of a singleton class will be pointing on the same object.
    """
    def __init__(self):
        # logger for library-related messages
        log = logging.getLogger(__name__)
        ch = logging.StreamHandler(stream=sys.stdout)
        if ['debug'] == 1:
            print('elo')
        log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s',
                                      datefmt='%H:%M:%S')
        ch.setFormatter(formatter)
        log.addHandler(ch)

        recognize_alg = Alpr(COUNTRY, PATH_TO_CONF, PATH_TO_RUN_TIME)

        # verify library's availability
        if not recognize_alg.is_loaded():
            log.error("Error loading a library")
        else:
            log.info("Starting detection process...")

        # TODO: clean up unnecessary parameters, given by default
        recognize_alg.set_top_n(1)
        recognize_alg.set_country(COUNTRY)
        recognize_alg.set_default_region(REGION)


class ImageAnalyseInt(ABC):
    @staticmethod
    @abstractmethod
    def analyse(_id, frame) -> []:
        pass


class ImageAnalyse(ImageAnalyseInt):
    @staticmethod
    def analyse(_id, frame) -> []:
        """
        Analyse function uses pre-initialized ML instance to analyse an image.
        :param _id: unique process identifier.
        :param frame: dataclass object containing a frame for the analysis.
        :return: a list of LicensePlate objects referring to the found plates.
        """
        ml_instance = MLInstance()
        # model requires bytes array, so read image in binary mode
        # TODO define frame
        # jpeg_bytes = open(frame, "rb").read()
        jpeg_bytes = bytes(frame)
        results = ml_instance.recognize_alg.recognize_array(jpeg_bytes)

        plates = []
        for regions in results['results']:
            plate = LicensePlate.LicensePlate(str(regions['plate']), float(regions['confidence']),
                                              dict(regions['coordinates']), float(regions['processing_time_ms']))
            plates.append(plate)
        return plates


class ImageAnalyseMock(ImageAnalyseInt):
    @staticmethod
    def analyse(_id, frame: Frame) -> LicensePlate:
        time.sleep(random.uniform(0.01, 0.05))
        return LicensePlate(id_=frame.id_)
