import os
import time

import toml
from core.manager.Manager import Manager
import logging


def test_windows_mock():
    with open("core/tests/test_config.toml") as file:
        config = toml.load(file)
    config['mock'] = 1

    manager = Manager(config)
    manager.run()

    while manager.get_status():
        pass

    assert os.path.isfile('core/tests/test_log.log') is True


def test_windows():
    with open("core/tests/test_config.toml") as file:
        config = toml.load(file)
    config['mock'] = 0
    config['input']['video_input_path'] = '../../grupaA1.mp4'

    manager = Manager(config)
    manager.run()

    while manager.get_status():
        pass

    time.sleep(5)

    assert os.path.isfile('core/tests/test_log.log') is True

    with open('core/tests/test_log.log', 'r') as f:
        Lines = f.readlines()
        for line in Lines:
            logging.info(line)
