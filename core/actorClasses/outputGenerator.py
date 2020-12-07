import logging
import sys
from typing import Dict

import cv2
import numpy as np
from cv2.cv2 import VideoWriter_fourcc, VideoWriter
from rx.subject import Subject

from core.dataClasses.frame import Frame


class OutputGenerator:
    def __init__(self, log_file_path: str, analysed_frames: Subject, status_callback: Subject):

        self.log = logging.getLogger(__name__)
        ch = logging.StreamHandler(stream=sys.stdout)
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s',
                                      datefmt='%H:%M:%S')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        self._log_file_path = log_file_path
        self._analysed_frames = analysed_frames

        self._logs: Dict[int, Frame] = {}
        self._status_callback = status_callback

        self._last_analysed_id = 0

    def generate_log_file(self):
        """
        generates log file as output
        """
        self.log.debug("Started collecting logs")

        self._analysed_frames.subscribe(
            on_next=lambda f: self._on_next(f),
            on_error=lambda e: self.log.error(e),
            on_completed=lambda: self._on_completed()
        )

    def _on_next(self, frame: Frame):
        self._logs[frame.id_] = frame

    def _on_completed(self):
        self.log.info('Writing logs to file')
        with open(self._log_file_path + '.log', "w+") as file:
            _name = self._log_file_path + '.mp4'
            _fourcc = VideoWriter_fourcc(*'mp4v')
            _y, _x, _ = self._logs[1].img_.shape
            _out = VideoWriter(_name, _fourcc, self._logs[1].fps_, (_x, _y))

            length = len(self._logs)
            for i in range(0, length):

                if not self._logs[i].is_analysed_:
                    index = i
                    while index in self._logs:
                        # TODO temporary solution
                        if self._logs[index].is_analysed_:
                            break
                        index = index - 1
                    if index in self._logs:
                        self._logs[i].license_plates_ = self._logs[index].license_plates_
                frame = self._logs[i]
                file.write(str(frame.id_) + ':' + str(frame) + '\n')

                for _plates in self._logs[i].license_plates_:
                    pts = np.array([[e['x'], e['y']] for e in _plates.coordinates], np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(self._logs[i].img_, [pts], True, (0, 20, 200), thickness=2)

                _out.write(frame.img_)
        self._status_callback.on_completed()
