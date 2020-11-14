import logging
import queue
import sys
import threading
from concurrent.futures.thread import ThreadPoolExecutor

from core.actorClasses.imageAnalyse import ImageAnalyseMock, ImageAnalyse
from core.actorClasses.imageProcessing import ImageProcessingMock, ImageProcessing
from core.actorClasses.outputGenerator import OutputGenerator
from core.dataClasses.frame import Frame
from core.dataClasses.signal import Signal


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class Manager:
    def __init__(self, _config):
        """
        default constructor for Manager class
        :param _config: dictionary containing current configuration
        """
        self._debug = _config['debug']
        self._mock = _config['mock']

        self.log = logging.getLogger(__name__)

        ch = logging.StreamHandler(stream=sys.stdout)
        if self._debug == 1:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s|%(threadName)s|%(name)s|%(levelname)s|%(message)s',
                                      datefmt='%H:%M:%S')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        self._max_workers = _config['manager']['max_workers']
        self._executor = ThreadPoolExecutor(max_workers=self._max_workers)
        self._futures = []

        self._producer_queue = queue.Queue(maxsize=5)
        self._processing_queue = queue.Queue(maxsize=5)
        self._management_queue = queue.Queue(maxsize=2)
        self._log_queue = queue.Queue(maxsize=10)
        self._video_queue = queue.Queue(maxsize=10)

        self._is_processing_running = True
        self._is_analyse_running = True
        self._status = Signal.MAN_RUNNING

        self._show_futures_status = _config['logging']['show_futures_status']
        self._log_file_path = _config['output']['log_file_path']

        if self._mock == 0:
            self._img_processing_class = ImageProcessing
            self._img_analyse_class = ImageAnalyse
        else:
            self.log.warning("MOCK are classes used")
            self._img_processing_class = ImageProcessingMock
            self._img_analyse_class = ImageAnalyseMock

    def _management(self):
        while True:
            signal = self._management_queue.get()
            if signal == Signal.IMG_PROCESSING_FINISHED:
                self._is_processing_running = False
            elif signal == Signal.MAN_SUBMITTING_FINISHED:
                break
            self._management_queue.task_done()
        self._status = Signal.MAN_STOPPED
        self.log.info("_management task finished")

    def run(self):
        """

        :return:
        """
        threading.Thread(target=self._management).start()

        _imgProcessing = self._img_processing_class(self._processing_queue, self._management_queue)
        threading.Thread(target=_imgProcessing.process).start()
        threading.Thread(target=self._submit_tasks).start()
        threading.Thread(target=self._listen_and_send).start()

        self.log.info("run finished execution")

    def _submit_tasks(self):
        while self._is_processing_running:
            imgFrame: Frame = self._processing_queue.get()
            if imgFrame is None:
                break
            fut = self._executor.submit(self._img_analyse_class.analyse, 1, imgFrame, self._producer_queue)
            fut.add_done_callback(self._callback)

            self._futures.append(fut)
            self._processing_queue.task_done()
        self.log.info('(img_processing) no more tasks to submit')
        self._executor.shutdown(wait=True)
        self._futures.clear()
        self._producer_queue.put(None)
        self._is_analyse_running = False

        # temporary switch for _management method
        self._management_queue.put(Signal.MAN_SUBMITTING_FINISHED)

        self.log.info('submitting tasks finished')

    def _callback(self, fn):
        """
        callback method is called after each future finishes. It clears associated future
        and if specified in config logs frame info
        :param fn:
        :return:
        """
        if fn.cancelled():
            self.log.warning('canceled')
        elif fn.done():
            error = fn.exception()
            if error:
                self.log.error('error returned: {}'.format(error))
            else:
                if self._show_futures_status == 1:
                    self.log.info('value returned: {}'.format(fn.result()))
        self._futures.remove(fn)

    def _listen_and_send(self):
        output_gen = OutputGenerator(self._log_file_path, self._log_queue)
        threading.Thread(target=output_gen.generate_log_file).start()

        while self._is_analyse_running:
            res = self._producer_queue.get()
            self._log_queue.put(res)
            if res is None:
                break
            self.log.debug(res)
        self._log_queue.put(None)
        self.log.info('DONE')

    def mock(self):
        return self._max_workers

    def get_status(self):
        return self._status


if __name__ == '__main__':
    import toml

    with open("../../config.toml") as file:
        config = toml.load(file)

    manager = Manager(config)
    manager.run()
