import pytest

from src.configs.default_config import DefaultConfig
from src.configs.development_config import DevelopmentConfig


class TestDevelopmentConfig:
    @pytest.mark.unit
    def test_inherits_default_config(self) -> None:
        config: DevelopmentConfig = DevelopmentConfig()
        assert isinstance(config, DefaultConfig)

    @pytest.mark.unit
    def test_debug_is_true(self) -> None:
        config: DevelopmentConfig = DevelopmentConfig()
        assert config.DEBUG is True

    @pytest.mark.unit
    def test_env_is_development(self) -> None:
        config: DevelopmentConfig = DevelopmentConfig()
        assert config.ENV == "development"

    @pytest.mark.unit
    def test_testing_is_false(self) -> None:
        config: DevelopmentConfig = DevelopmentConfig()
        assert config.TESTING is False

    @pytest.mark.unit
    def test_has_env_name(self) -> None:
        config: DevelopmentConfig = DevelopmentConfig()
        assert hasattr(config, "ENV_NAME")
