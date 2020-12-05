import os
import time

import toml
from core.manager.Manager import Manager


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
