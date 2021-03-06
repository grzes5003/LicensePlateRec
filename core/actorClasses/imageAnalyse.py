import logging
import os
import random
import sys
import threading
import time
from abc import abstractmethod, ABC
from pathlib import Path

import cv2

from core.dataClasses.LicensePlate import LicensePlate
from core.dataClasses.frame import Frame
from openalpr_x86.python.build.lib.openalpr.openalpr import Alpr

# module files are inside another directory, so python dirs search should be expanded
ROOT_DIR = Path(__file__).parent.parent.parent
if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(os.path.dirname(sys.executable)).resolve()

PATH_TO_CONF = Path.joinpath(ROOT_DIR, "openalpr_x86", "config.alpr.conf")
PATH_TO_RUN_TIME = Path.joinpath(ROOT_DIR, "openalpr_x86", "runtime_data")
COUNTRY = "eu"
REGION = "pl"


class SingletonThread(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        _id = threading.get_ident()
        if _id not in cls._instances:
            cls._instances[_id] = {}
        if cls not in cls._instances[_id]:
            cls._instances[_id][cls] = super(SingletonThread, cls).__call__(*args, **kwargs)
        return cls._instances[_id][cls]


class MLInstance(metaclass=SingletonThread):
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
        log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s ML- %(name)s - %(threadName)s - %(levelname)s - %(message)s',
                                      datefmt='%H:%M:%S')
        ch.setFormatter(formatter)
        log.addHandler(ch)

        self.recognize_alg = Alpr(bytes(COUNTRY, encoding='utf-8'), bytes(str(PATH_TO_CONF), encoding='utf-8'),
                                  bytes(str(PATH_TO_RUN_TIME), encoding='utf-8'))

        # verify library's availability
        if not self.recognize_alg.is_loaded():
            log.error("Error loading a library")
        else:
            # log.info("Starting detection process...")
            pass

        # TODO: clean up unnecessary parameters, given by default
        # self.recognize_alg.set_top_n(5)
        # self.recognize_alg.set_country(COUNTRY)
        self.recognize_alg.set_default_region(bytes(REGION, encoding='utf-8'))


class ImageAnalyseInt(ABC):
    @staticmethod
    @abstractmethod
    def analyse(frame: Frame) -> Frame:
        """
        Analyse method searches for license plate on particular frame, as an result
        it modifies LicensePlates array.
        :param frame:
        :return:
        """
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
        logging.debug("ENTERED ANALYSE")

        ml_instance = MLInstance()
        # model requires bytes array, so read image in binary mode
        gray = cv2.cvtColor(frame.img_, cv2.COLOR_BGR2GRAY)
        _, jpeg_bytes = cv2.imencode('.jpg', gray)
        jpeg_bytes = jpeg_bytes.tobytes()

        results = ml_instance.recognize_alg.recognize_array(jpeg_bytes)

        for regions in results['results']:
            plate = LicensePlate(str(regions['plate']), float(regions['confidence']),
                                 regions['coordinates'], float(regions['processing_time_ms']))
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
