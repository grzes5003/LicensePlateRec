import logging
import sys


class OutputGenerator:
    def __init__(self, log_file_path, log_queue):

        self.log = logging.getLogger(__name__)
        ch = logging.StreamHandler(stream=sys.stdout)
        if ['debug'] == 1:
            print('elo')
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        self._log_file_path = log_file_path
        self._log_queue = log_queue

    def generate_log_file(self):
        """
        generates log file as output
        :return: status
        """
        logs = {}
        self.log.debug("enters")

        while True:
            frame = self._log_queue.get()
            # self.log.debug("new frame %s", frame)
            if frame is None:
                break
            logs[frame.value] = str(frame.value) + ':' + str(frame) + '\n'
            self._log_queue.task_done()
        self.log.debug("out of while True")

        with open(self._log_file_path, "w+") as file:
            length = len(logs)
            for i in range(0, length):
                file.write(logs[i])
        return 0
