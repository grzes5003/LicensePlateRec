import filecmp
import os
import time

from core.manager.Manager import Manager


def test_manager_mocks():
    import toml

    # TODO temporary test disable
    return
    with open("core/tests/test_config.toml") as file:
        config = toml.load(file)

    manager = Manager(config)
    manager.run()

    while manager.get_status():
        pass

    # TODO add signal from generator it has generated output
    time.sleep(1)
    print(os.listdir('core/tests/'))

    assert os.path.isfile('core/tests/test_target_log.log') is True
    assert os.path.isfile('core/tests/test_log.log') is True
    assert filecmp.cmp('core/tests/test_target_log.log', 'core/tests/test_log.log', shallow=True) is True
