# This Python file uses the following encoding: utf-8
import logging
import os
import sys
import threading
import traceback
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname, urljoin

import cv2
from PySide2.QtCore import QObject, Slot, QUrl
from PySide2.QtWidgets import QMessageBox, QWidget

from core.manager.Manager import Manager


class MainWindow(QObject):
    def __init__(self, root, manager: Manager):
        QObject.__init__(self)

        # logger declaration
        self.log = logging.getLogger(__name__)
        ch = logging.StreamHandler(stream=sys.stdout)
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s|%(threadName)s|%(name)s|%(lineno)d|%(levelname)s|%(message)s',
                                      datefmt='%H:%M:%S')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)
        # end of logger declaration

        self._root = root
        self.counter = 0
        self.video_path = ''
        self.dest_path = os.path.join(os.path.dirname(__file__))
        self._log_file_dest = ''
        self._manager = manager

        self.is_analysed = False
        self.is_locked = False

        self.analyse_btn = self._root.findChild(QObject, "btn_analyze")
        # self.analyse_btn.setEnabled(False)

        sys.excepthook = MainWindow.excepthook

    @Slot(str, result=str)
    def getSourceVid(self, file_path):
        self.counter += 1

        print("Wybrales " + file_path)

        self.video_path = file_path

        video = cv2.VideoCapture(self.video_path)
        if video.isOpened():
            ret, frame = video.read()

            frame = cv2.resize(frame, (283, 178))
            image = self._root.findChild(QObject, "image")

            # A way to force QComponent to reload image, not really elegant but it works

            # works on macos, no idea how behaves on windows :)
            if self.counter % 2:
                cv2.imwrite(url2pathname(urlparse(urljoin(os.path.dirname(self.video_path), "preview1.png")).path), frame)
                # url2pathname(urlparse(os.path.join(os.path.dirname(self.video_path), "preview1.png")).path)
                url = QUrl(urljoin(os.path.dirname(self.video_path), "preview1.png"))
            else:
                cv2.imwrite(url2pathname(urlparse(urljoin(os.path.dirname(self.video_path), "preview2.png")).path), frame)
                url = QUrl(urljoin(os.path.dirname(self.video_path), "preview2.png"))
            image.setProperty("source", url)

            txt_status = self._root.findChild(QObject, "txt_status")
            txt_status.setProperty("text", "Status: Ready")

            txt_name = self._root.findChild(QObject, "txt_name")
            txt_name.setProperty("text", "Name: " + self.video_path.rpartition('/')[2])

            fps = video.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
            frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps
            print(int(duration))
            txt_duration = self._root.findChild(QObject, "txt_duration")
            txt_duration.setProperty("text",
                                     "Duration: " + str(int(duration / 60)) + " min " + str(int(duration % 60)) + " s")

        video.release()

        src = self.video_path.rpartition('/')[0][8:]
        if len(src) > 36:
            src = src[0:18] + "..." + src[len(src) - 18:] + '/'

        return "Source: " + src

    @Slot(str, result=str)
    def getDestFolder(self, folder_path):
        self.dest_path = folder_path
        self.log.info("destination path: " + folder_path)

        dest = self.dest_path
        print(dest)
        if len(dest) > 36:
            dest = dest[0:18] + "..." + dest[len(dest) - 18:]
        return "Destination: " + dest

    @Slot()
    def openVideo(self):
        self.log.info(self.video_path)
        if not self.dest_path or not self.is_analysed or self.is_locked:
            popup_not_found = self._root.findChild(QObject, "popup_not_found")
            popup_not_found.open()
            return
        os.startfile(url2pathname(urlparse(self.video_path).path))

    @Slot()
    def openLog(self):
        self.log.info(self._log_file_dest)
        if not self.dest_path or not self.is_analysed or self.is_locked:
            popup_not_found = self._root.findChild(QObject, "popup_not_found")
            popup_not_found.open()
            return
        os.startfile(self._log_file_dest + '.log')

    @Slot()
    def startAnalyze(self):
        popup_warning = self._root.findChild(QObject, "popup_warning")
        progbar = self._root.findChild(QObject, "progressBar")
        if not self.dest_path or not self.video_path:
            popup_warning.open()
            return
        if self.is_locked:
            return
        self.is_analysed = False
        self.is_locked = True
        progbar.setProperty("value", 0)
        thr = threading.Thread(target=self.analyze)
        thr.start()

    def analyze(self):
        progbar = self._root.findChild(QObject, "progressBar")
        self.log.debug(Path(__file__).resolve())
        progbar.setProperty("value", 0.1)

        file_name = str(os.path.basename(self.video_path)).split('.')[0] + '_log'

        dest_path = os.path.join(urlparse(self.dest_path).path, file_name)
        video_path = urlparse(self.video_path).path
        self._log_file_dest = url2pathname(dest_path)
        self._manager.reset_config(video_input_path=url2pathname(video_path),
                                   log_file_path=url2pathname(dest_path))
        self._manager.run()

        while self._manager.get_status():
            progbar.setProperty("value", self._manager.get_progress())
        progbar.setProperty("value", 1)
        self.log.info("Finished analysing")

        self.is_analysed = True
        self.is_locked = False
        popup_success = self._root.findChild(QObject, "popup_success")
        popup_success.open()
        progbar.setProperty("value", 0)

    @staticmethod
    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)

# def run():
#     app = QGuiApplication(sys.argv)
#     engine = QQmlEngine()
#
#     component = QQmlComponent(engine)
#     component.loadUrl(QUrl('main.qml'))
#
#     root = component.create()
#
#     mainWindow = MainWindow(root)
#
#     # Expose the Python object to QML
#     context = engine.rootContext()
#     context.setContextProperty("con", mainWindow)
#
#     return app.exec_()
#
#
# if __name__ == "__main__":
#     sys.exit(run())
