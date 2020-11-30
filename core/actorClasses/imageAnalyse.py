import random
import time
import logging
import sys
import os
from abc import abstractmethod, ABC
from core.dataClasses import LicensePlate
from pathlib import Path

from core.dataClasses.LicensePlate import LicensePlate
from core.dataClasses.frame import Frame

# module files are inside another directory, so python dirs search should be expanded
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(Path.joinpath(ROOT_DIR, "openalpr"))
from alpr.lprec import Alpr

PATH_TO_CONF = Path.joinpath(ROOT_DIR, "alpr", "config.alpr.conf")
PATH_TO_RUN_TIME = Path.joinpath(ROOT_DIR, "alpr", "runtime-data")
COUNTRY = "eu"
REGION = "pl"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MLInstance(metaclass=Singleton):
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

        recognize_alg = Alpr(COUNTRY, str(PATH_TO_CONF), str(PATH_TO_RUN_TIME))

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
    def analyse(frame: Frame) -> Frame:
        raise NotImplemented


class ImageAnalyse(ImageAnalyseInt):
    @staticmethod
    def analyse(frame: Frame) -> Frame:
        """
        # TODO change
        Analyse function uses pre-initialized ML instance to analyse an image.
        :param frame: dataclass object containing a frame for the analysis.
        :return: Modified frame containing a list of LicensePlate objects referring to the found plates.
        """
        ml_instance = MLInstance()
        # model requires bytes array, so read image in binary mode
        # TODO define frame
        # jpeg_bytes = open(frame, "rb").read()
        jpeg_bytes = bytes(frame.img_)
        results = ml_instance.recognize_alg.recognize_array(jpeg_bytes)

        for regions in results['results']:
            plate = LicensePlate.LicensePlate(str(regions['plate']), float(regions['confidence']),
                                              dict(regions['coordinates']), float(regions['processing_time_ms']))
            frame.license_plates_.append(plate)
        return frame


class ImageAnalyseMock(ImageAnalyseInt):
    @staticmethod
    def analyse(frame: Frame) -> Frame:
        rand_number_ = random.uniform(0.01, 0.05)
        time.sleep(rand_number_)
        coord_dict_ = {
            'x': 1,
            'y': 2
        }
        # if rand_number_ > 0.03:
        #     frame.license_plates_.append(LicensePlate(str(frame.id_)*5, 0.9, coord_dict_, 100))
        #     frame.license_plates_.append(LicensePlate(str(frame.id_+1) * 5, 0.7, coord_dict_, 96))
        # elif rand_number_ < 0.03:
        #     frame.license_plates_.append(LicensePlate(str(frame.id_) * 5, 0.9, coord_dict_, 100))
        frame.license_plates_.append(LicensePlate(str(frame.id_) * 5, 0.9, coord_dict_, 100))
        return frame
