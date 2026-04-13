import pytest

from src.configs.default_config import DefaultConfig
from src.configs.production_config import ProductionConfig


class TestProductionConfig:
    @pytest.mark.unit
    def test_inherits_default_config(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert isinstance(config, DefaultConfig)

    @pytest.mark.unit
    def test_debug_is_false(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert config.DEBUG is False

    @pytest.mark.unit
    def test_env_is_production(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert config.ENV == "production"

    @pytest.mark.unit
    def test_testing_is_false(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert config.TESTING is False

    @pytest.mark.unit
    def test_has_env_name(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert hasattr(config, "ENV_NAME")
