import pytest

from src.configs.default_config import DefaultConfig


class TestDefaultConfig:
    @pytest.mark.unit
    def test_debug_is_false(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert config.DEBUG is False

    @pytest.mark.unit
    def test_testing_is_false(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert config.TESTING is False

    @pytest.mark.unit
    def test_env_name_from_pytest_env(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert config.ENV_NAME == "template_value"

    @pytest.mark.unit
    def test_tz_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("TZ", raising=False)
        config: DefaultConfig = DefaultConfig()
        assert config.TZ == "America/Argentina/Buenos_Aires"

    @pytest.mark.unit
    def test_tz_from_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("TZ", "UTC")
        config: DefaultConfig = DefaultConfig()
        assert config.TZ == "UTC"

    @pytest.mark.unit
    def test_env_name_from_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENV_NAME", "my-game")
        config: DefaultConfig = DefaultConfig()
        assert config.ENV_NAME == "my-game"
