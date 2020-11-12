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

    assert os.path.isfile('./test_target_log.log') is True
    assert os.path.isfile('./test_log.log') is True
    assert filecmp.cmp('./test_target_log.log', './test_log.log', shallow=False) is True
