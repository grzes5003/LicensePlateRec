import pytest
from core.manager.Manager import Manager


class TestBasicConfig:

    def test_proper_import(self):
        import toml

        with open("./test_config.toml") as file:
            config = toml.load(file)

        manager = Manager(config)
        res = manager.mock()

        assert config['manager']['max_workers'] is res
