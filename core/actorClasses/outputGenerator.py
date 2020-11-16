import logging
import sys

from rx.subject import Subject
from rx import create

from core.dataClasses.LicensePlate import LicensePlate


class OutputGenerator:
    def __init__(self, log_file_path: str, analysed_frames: Subject, status_callback: Subject):

        self.log = logging.getLogger(__name__)
        ch = logging.StreamHandler(stream=sys.stdout)
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        self._log_file_path = log_file_path
        self._analysed_frames = analysed_frames

        self._logs = {}
        self._status_callback = status_callback

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

    def _on_next(self, license_plate: LicensePlate):
        self._logs[license_plate.id_] = str(license_plate.id_) + ':' + str(license_plate) + '\n'

    def _on_completed(self):
        self.log.info('Writing logs to file')
        with open(self._log_file_path, "w+") as file:
            length = len(self._logs)
            for i in range(0, length):
                file.write(self._logs[i])
        self._status_callback.on_completed()


