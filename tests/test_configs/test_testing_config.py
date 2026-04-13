import pytest

from src.configs.default_config import DefaultConfig
from src.configs.testing_config import TestingConfig


class TestTestingConfig:
    @pytest.mark.unit
    def test_inherits_default_config(self) -> None:
        config: TestingConfig = TestingConfig()
        assert isinstance(config, DefaultConfig)

    @pytest.mark.unit
    def test_testing_is_true(self) -> None:
        config: TestingConfig = TestingConfig()
        assert config.TESTING is True

    @pytest.mark.unit
    def test_debug_is_true(self) -> None:
        config: TestingConfig = TestingConfig()
        assert config.DEBUG is True

    @pytest.mark.unit
    def test_env_is_testing(self) -> None:
        config: TestingConfig = TestingConfig()
        assert config.ENV == "testing"

    @pytest.mark.unit
    def test_env_name_from_pytest_env(self) -> None:
        config: TestingConfig = TestingConfig()
        assert config.ENV_NAME == "template_value"
