import filecmp
import os

from core.dataClasses.signal import Signal
from core.manager.Manager import Manager


def test_manager_mocks():
    import toml

    with open("core/tests/test_config.toml") as file:
        config = toml.load(file)

    manager = Manager(config)
    manager.run()

    while manager.get_status() == Signal.MAN_RUNNING:
        pass

    print(os.listdir('core/tests/'))

    assert os.path.isfile('core/tests/test_target_log.log') is True
    assert os.path.isfile('core/tests/test_log.log') is True
    assert filecmp.cmp('core/tests/test_target_log.log', 'core/tests/test_log.log', shallow=True) is True
