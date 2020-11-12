from core.manager.Manager import Manager


def test_proper_import():
    import toml

    with open("./test_config.toml") as file:
        config = toml.load(file)

    manager = Manager(config)
    res = manager.mock()

    assert config['manager']['max_workers'] is res
