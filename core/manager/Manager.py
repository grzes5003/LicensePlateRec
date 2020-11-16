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

from rx import create, operators as ops
from rx.subject import Subject


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

        # logger declaration
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
        # end of logger declaration

        self._max_workers = _config['manager']['max_workers']
        self._executor = ThreadPoolExecutor(max_workers=self._max_workers)
        self._futures = []

        self._show_futures_status = _config['logging']['show_futures_status']
        self._log_file_path = _config['output']['log_file_path']

        self._analysed_frames = Subject()
        self._file_generation_status = True

        if self._mock == 0:
            self._img_processing_class = ImageProcessing
            self._img_analyse_class = ImageAnalyse
        else:
            self.log.warning("MOCK classes are used")
            self._img_processing_class = ImageProcessingMock
            self._img_analyse_class = ImageAnalyseMock

    def run(self):
        """
        method starts image processing, analysis and output generation.
        :return:
        """
        threading.Thread(target=self._collect_img_processing).start()
        threading.Thread(target=self._generate_log_file).start()

    def _collect_img_processing(self):
        """
        Method creates instance of image processing class.
        Handles all incoming Frames, passing it to ThreadPoolExecutor to be analysed.
        :return:
        """
        _img_processing_instance = self._img_processing_class()
        _img_processing_source = create(_img_processing_instance.process)

        _img_processing_source.subscribe(
            on_next=lambda f: self._on_next(f),
            on_error=lambda e: self.log.error(e),
            on_completed=lambda: self.log.info('Img processing has been completed')
        )

        self._executor.shutdown(wait=True)
        self._futures.clear()
        self._analysed_frames.on_completed()

    def _on_next(self, frame):
        """
        Passes incoming Frame to self._executor for analysis.
        :param frame: instance of Frame class
        :return:
        """
        fut = self._executor.submit(self._img_analyse_class.analyse, 1, frame)
        fut.add_done_callback(self._callback)
        self._futures.append(fut)

    def _callback(self, fn):
        """
        callback method is called after each future finishes.
        It sends analysed LicencePlate to self._analysed_frames.
        It also clears associated future and if specified in config logs frame info.
        :param fn: frame returned by _img_analyse_class.analyse
        :return:
        """
        if fn.cancelled():
            self.log.warning('canceled')
            self._analysed_frames.on_error(Exception("Job was cancelled"))
        elif fn.done():
            error = fn.exception()
            if error:
                self.log.error('error returned: {}'.format(error))
                self._analysed_frames.on_error(error)
            else:
                if self._show_futures_status == 1:
                    self.log.info('value returned: {}'.format(fn.result()))
                self._analysed_frames.on_next(fn.result())
        self._futures.remove(fn)

    def _generate_log_file(self):
        """
        It invokes Output Generation process.
        :return:
        """
        self._file_generation_status = True
        output_gen = OutputGenerator(self._log_file_path, self._analysed_frames)
        output_gen.generate_log_file()
        self._file_generation_status = False

    def mock(self):
        """
        Just for test purposes
        :return:
        """
        return self._max_workers

    def get_status(self):
        return self._file_generation_status


if __name__ == '__main__':
    import toml

    with open("../../config.toml") as file:
        config = toml.load(file)

    manager = Manager(config)
    manager.run()
