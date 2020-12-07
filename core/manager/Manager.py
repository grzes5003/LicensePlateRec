import logging
import sys
import threading
from concurrent.futures.process import ProcessPoolExecutor

from rx import create, operators as ops
from rx.subject import Subject

from core.actorClasses.imageAnalyse import ImageAnalyseMock, ImageAnalyse
from core.actorClasses.imageProcessing import ImageProcessingMock, ImageProcessing
from core.actorClasses.outputGenerator import OutputGenerator
from core.dataClasses.frame import Frame


def singleton(class_):
    """
    decorator used as a form of singleton design pattern implementation
    :param class_:
    :return:
    """
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
        :param _config: dictionary containing current configuration (from a *config.toml file)
        """
        self._debug = _config['debug']
        self._mock = _config['mock']
        self._nth_analysed = _config['manager']['nth_analysed']
        self._video_input_path = _config['input']['video_input_path']

        # logger declaration
        self.log = logging.getLogger(__name__)

        ch = logging.StreamHandler(stream=sys.stdout)
        if self._debug == 1:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s|%(threadName)s|%(name)s|%(lineno)d|%(levelname)s|%(message)s',
                                      datefmt='%H:%M:%S')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)
        # end of logger declaration

        self._max_workers = _config['manager']['max_workers']
        self._executor = ProcessPoolExecutor(max_workers=self._max_workers)
        self._futures = []

        self._show_futures_status = _config['logging']['show_futures_status']
        self._log_file_path = _config['output']['log_file_path']

        # Two streams (Subjects) used as communication channels with OutputGenerator
        self._analysed_frames = Subject()
        self._generate_log_status = Subject()
        # status of log generating class instance, currently used only in basic mock test (True=busy)
        self._file_generation_status = True

        if self._mock == 0:
            self._img_processing_class = ImageProcessing
            self._img_analyse_class = ImageAnalyse
        else:
            self.log.warning("MOCK classes are used")
            self._img_processing_class = ImageProcessingMock
            self._img_analyse_class = ImageAnalyseMock

        # self._last_analysed_frame = Frame(-1)
        self.log.info('Path to input file: %s', self._video_input_path)

        self._are_all_processed = False

    def run(self):
        """
        method starts image processing, analysis and output generation.
        It creates appropriate threads for:
            _collect_img_processing: starting processing and collecting images
            _generate_log_file: starting generation of output log file
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
        _img_processing_instance = self._img_processing_class(self._video_input_path)
        _img_processing_source = create(_img_processing_instance.process)

        def on_complete_processing():
            self.log.info('Img processing has been completed')
            self._are_all_processed = True

        _img_processing_source.pipe(ops.filter(lambda f: self._filter(f))).subscribe(
            on_next=lambda f: self._on_next(f),
            on_error=lambda e: self.log.error(e),
            on_completed=lambda: on_complete_processing()
        )

        self._executor.shutdown(wait=True)
        self._futures.clear()
        self._analysed_frames.on_completed()

    def _filter(self, frame: Frame) -> bool:
        """
        filtering method is used by incoming processed images stream.
        It passes every nth frame to be analysed, to optimise program execution.
        Rest of the frames are directly passed to the Output generator instance.
        :param frame: Frame: input Frame
        :return: boolean: based on frame id_ returns True or False
        """
        if frame.id_ % self._nth_analysed == 0:
            frame.is_analysed_ = True
            return True
        # self._last_analysed_frame.id_ = frame.id_
        self._analysed_frames.on_next(frame)
        return False

    def _on_next(self, frame: Frame):
        """
        Passes incoming processed image (from ImgProcessing) as Frame to self._executor for analysis.
        :param frame: instance of a Frame class
        :return:
        """
        fut = self._executor.submit(self._img_analyse_class.analyse, frame)
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
        The _generate_log_status is stream (emitter is OutputGenerator) containing status.
        _analysed_frames is stream of analysed Frames with [LicensePlates].
        :return:
        """

        def _switch_status():
            self._file_generation_status = False
            self.log.info("_file_generation_status set to false")

        self._generate_log_status.subscribe(
            on_next=lambda m: self.log.info('Output generator status: {}'.format(m)),
            on_error=lambda e: self.log.error('Output generator error: {}'.format(e)),
            on_completed=lambda: _switch_status(),
        )

        self._file_generation_status = True
        output_gen = OutputGenerator(self._log_file_path, self._analysed_frames, self._generate_log_status)
        output_gen.generate_log_file()

    def mock(self):
        """
        Just for test purposes
        :return:
        """
        return self._max_workers

    def get_status(self):
        """
        DEPRECATED
        TO BE REMOVED IN FUTURE
        :return:
        """
        return self._file_generation_status

    def get_progress(self) -> float:
        """
        Returns number between 0 and 1,
        indicating progress file analysing
        :return: float: between 0 and 1
        """
        if self._are_all_processed:
            if self._generate_log_status:
                return 1
            return 0.3
        return 0.1

    def reset_config(self, video_input_path=None, log_file_path=None):

        if video_input_path is not None:
            self._video_input_path = video_input_path

        if log_file_path is not None:
            self._log_file_path = log_file_path

        # Two streams (Subjects) used as communication channels with OutputGenerator
        self._analysed_frames = Subject()
        self._generate_log_status = Subject()
        # status of log generating class instance, currently used only in basic mock test (True=busy)
        self._file_generation_status = True

        # self._last_analysed_frame = Frame(-1)
        self.log.info('Path to input file: %s', self._video_input_path)

        self._are_all_processed = False


if __name__ == '__main__':
    import toml

    with open("../../config.toml") as file:
        config = toml.load(file)

    manager = Manager(config)
    manager.run()
