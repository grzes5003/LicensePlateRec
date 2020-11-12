import filecmp

from core.manager.Manager import Manager


def test_manager_mocks():
    import toml

    with open("core/tests/test_config.toml") as file:
        config = toml.load(file)

    manager = Manager(config)
    manager.run()

    assert filecmp.cmp('core/tests/test_target_log.log', 'core/tests/test_log.log', shallow=False) is True
