import sys
from pathlib import Path

import toml
from PySide2.QtCore import QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlComponent, QQmlEngine

from core.manager.Manager import Manager
from gui.main import MainWindow

from multiprocessing import freeze_support


if __name__ == '__main__':
    freeze_support()

    with open("config.toml") as file:
        config = toml.load(file)

    print(Path(__file__).resolve())

    manager = Manager(config)

    app = QGuiApplication(sys.argv)
    engine = QQmlEngine()

    component = QQmlComponent(engine)
    component.loadUrl(QUrl('gui/main.qml'))

    root = component.create()

    mainWindow = MainWindow(root, manager)

    # Expose the Python object to QML
    context = engine.rootContext()
    context.setContextProperty("con", mainWindow)

    sys.exit(app.exec_())
