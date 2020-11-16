import logging
import sys

from rx.subject import Subject


class OutputGenerator:
    def __init__(self, log_file_path, analysed_frames: Subject):

        self.log = logging.getLogger(__name__)
        ch = logging.StreamHandler(stream=sys.stdout)
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        self._log_file_path = log_file_path
        self._analysed_frames = analysed_frames

        self._logs = {}

    def generate_log_file(self):
        """
        generates log file as output
        """
        self.log.debug("enters")

        self._analysed_frames.subscribe(
            on_next=lambda f: self._on_next(f),
            on_error=lambda e: self.log.error(e),
            on_completed=lambda: self._on_completed()
        )

    def _on_next(self, frame):
        self._logs[frame.value] = str(frame.value) + ':' + str(frame) + '\n'

    def _on_completed(self):
        self.log.info('out of while True')
        with open(self._log_file_path, "w+") as file:
            length = len(self._logs)
            for i in range(0, length):
                file.write(self._logs[i])


