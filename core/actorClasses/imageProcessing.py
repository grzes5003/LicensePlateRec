import random
import time

import cv2
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

    def __init__(self, _path):
        self._path = _path

    def process(self, _observer, _scheduler):
        video = cv2.VideoCapture(self._path)

        if not video.isOpened():
            _observer.on_error('FILE NOT FOUND OR WRONG CODEC')

        # Find OpenCV version
        (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')

        if int(major_ver) < 3:
            fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            fps = video.get(cv2.CAP_PROP_FPS)

        curr_frame = 0
        while video.isOpened():
            ret, frame = video.read()

            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                f = Frame(curr_frame)
                f.time_stamp_ = curr_frame / fps
                f.img_ = gray
                _observer.on_next(f)
            else:
                break

            curr_frame += 1

        video.release()
        _observer.on_completed()


class ImageProcessingMock(ImageProcessingInt):
    def __init__(self, _):
        self._limit = 120

    def process(self, _observer, _scheduler):
        for i in range(self._limit):
            time.sleep(random.uniform(0.01, 0.05))
            # each time "send" processed image by evoking _observer.on_next( /analysed Frame/ ) method
            _observer.on_next(Frame(i))
        # when process is completed notify Manager by calling _observer.on_completed()
        _observer.on_completed()
