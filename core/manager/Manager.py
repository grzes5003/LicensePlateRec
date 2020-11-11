import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed, wait
from core.actorClasses.ImageProcessing import ImageProcessing
from core.actorClasses.ImageAnalyse import ImageAnalyse
import queue
import logging
import sys


class Manager:
    def __init__(self, max_workers, show_futures_status):
        self._max_workers = max_workers
        self._executor = ThreadPoolExecutor(max_workers=self._max_workers)
        self._futures = []
        self._producer_queue = queue.Queue(maxsize=5)
        self._is_running = True
        self._show_futures_status = show_futures_status

    # def run(self):
    #     with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
    #         _imgProcessing = ImageProcessing()
    #         futures = {
    #             executor.submit(ImageAnalyse.analyse, 1, task) for task in _imgProcessing.process()
    #         }
    #         print("cos")
    #         for fut in as_completed(futures):
    #             print(fut.result())

    def run(self):
        threading.Thread(target=self._submit_tasks).start()
        threading.Thread(target=self._listen_and_write).start()
        # wait(self._futures, return_when='FIRST_COMPLETED')
        # for future in as_completed(self._futures):
        #     print(future.result())
        log.info("done?")

    def _submit_tasks(self):
        _imgProcessing = ImageProcessing()
        for imgFrame in _imgProcessing.process():
            fut = self._executor.submit(ImageAnalyse.analyse, 1, imgFrame, self._producer_queue)
            if self._show_futures_status == 1:
                fut.add_done_callback(Manager._callback)
            self._futures.append(fut)
        self._executor.shutdown(wait=True)
        self._is_running = False
        log.info('done!')

    @staticmethod
    def _callback(fn):
        if fn.cancelled():
            print('canceled')
        elif fn.done():
            error = fn.exception()
            if error:
                print('error returned: {}'.format(error))
            else:
                result = fn.result()
                print('value returned: {}'.format(result))

    def _listen_and_write(self):
        while self._is_running:
            res = self._producer_queue.get()
            time.sleep(0.01)
            log.debug(res)
        log.info('DONE')


if __name__ == '__main__':
    import toml

    with open("../../config.toml") as file:
        config = toml.load(file)

    log = logging.getLogger(__name__)

    ch = logging.StreamHandler(stream=sys.stdout)
    if ['debug'] == 1:
        print('elo')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s -%(threadName)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # log.setLevel(logging.INFO)
    manager = Manager(config['manager']['max_workers'], config['logging']['show_futures_status'])
    manager.run()
