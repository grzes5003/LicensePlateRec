# This Python file uses the following encoding: utf-8
import os
import sys
from pathlib import Path

import cv2
import toml
from PySide2.QtCore import QObject, Slot, QUrl, QProcess


class MainWindow(QObject):
    def __init__(self, root):
        QObject.__init__(self)
        self._root = root
        self.counter = 0
        self.video_path = ''
        self.dest_path = ''
        self._p = QProcess()
        self.get_base_prefix_compat()

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
            if self.counter % 2:
                print("pr1")
                cv2.imwrite('preview1.png', frame)
                url = QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "preview1.png"))
                image.setProperty("source", url)
            else:
                print("pr2")
                cv2.imwrite('preview2.png', frame)
                url = QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "preview2.png"))
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
        print("Wybrales " + folder_path)

        dest = self.dest_path[8:]
        print(dest)
        if len(dest) > 36:
            dest = dest[0:18] + "..." + dest[len(dest) - 18:]
        return "Destination: " + dest

    @Slot()
    def openVideo(self):
        print(self.video_path)
        os.startfile(self.video_path)

    @Slot()
    def startAnalyze(self):
        progbar = self._root.findChild(QObject, "progressBar")
        progbar.setProperty("value", 0)
        # thr = threading.Thread(target=self.analyze)
        # thr.start()
        self.analyze()

    def analyze(self):
        progbar = self._root.findChild(QObject, "progressBar")
        import toml

        print(Path(__file__).resolve())

        with open("config.toml") as file:
            config = toml.load(file)

        self._p.readyReadStandardOutput.connect(self.handle_stdout)
        self._p.readyReadStandardError.connect(self.handle_stderr)
        if config['standalone'] == 0:
            self._p.start("python", ['mainCore.py', self.video_path[8:], self.dest_path[8:]])
            self._p.finished.connect(self.process_finished)
        progbar.setProperty("value", 0.1)

    def handle_stdout(self):
        data = self._p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        print(stdout)

    def handle_stderr(self):
        data = self._p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        print(stderr)

    def process_finished(self):
        progbar = self._root.findChild(QObject, "progressBar")
        progbar.setProperty("value", 1)
        self._p = None

    def get_base_prefix_compat(self):
        """Get base/real prefix, or sys.prefix if there is none."""
        print(getattr(sys, "base_prefix", None))
        print(getattr(sys, "real_prefix", None))
        print(getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix)

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
