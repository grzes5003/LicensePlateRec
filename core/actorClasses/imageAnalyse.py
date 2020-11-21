import random
import time
import pprint
import logging
import sys
from abc import abstractmethod, ABC
from openalpr import Alpr
from argparse import ArgumentParser
from core.dataClasses import LicensePlate

PATH_TO_CONF = "./openalpr/openalpr.myconfig.conf"
PATH_TO_RUN_TIME = "./runtime-data"
COUNTRY = "eu"
REGION = "pl"
from core.dataClasses.LicensePlate import LicensePlate
from core.dataClasses.frame import Frame


class ImageAnalyseInt(ABC):
    @staticmethod
    @abstractmethod
    def analyse(_id, frame: Frame) -> LicensePlate:
        pass


class ImageAnalyse(ImageAnalyseInt):
    @staticmethod
    def analyse(_id, frame, queue):
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

        recognize_alg.set_top_n(1)
        recognize_alg.set_country(COUNTRY)
        recognize_alg.set_default_region(REGION)

        # model requires bytes array, so read image in binary mode
        # TODO define frame
        # jpeg_bytes = open(frame, "rb").read()
        jpeg_bytes = bytes(frame)
        results = recognize_alg.recognize_array(jpeg_bytes)

        plate = None
        for regions in results['results']:
            plate = LicensePlate.LicensePlate(str(regions['plate']), float(regions['confidence']),
                                              dict(regions['coordinates']),  float(regions['processing_time_ms']))
            queue.put(plate)


class ImageAnalyseMock(ImageAnalyseInt):
    @staticmethod
    def analyse(_id, frame: Frame) -> LicensePlate:
        time.sleep(random.uniform(0.01, 0.05))
        return LicensePlate(id_=frame.id_)
