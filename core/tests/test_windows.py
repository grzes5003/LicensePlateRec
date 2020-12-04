import os

import toml
from core.manager.Manager import Manager


def test_windows_mock():
    with open("core/tests/test_config.toml") as file:
        config = toml.load(file)
    config['mock'] = 1

    manager = Manager(config)
    manager.run()

    while manager.get_status():
        pass

    assert os.path.isfile('core/tests/test_log.log') is True
