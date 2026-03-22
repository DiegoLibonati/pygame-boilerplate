from collections.abc import Generator
from typing import Any

import pygame
import pytest

from src.configs.default_config import DefaultConfig
from src.models.player_model import PlayerModel
from src.ui.interface_game import InterfaceGame


class MockKeys:
    def __init__(self, pressed: set[int] | None = None) -> None:
        self._pressed: set[int] = pressed or set()

    def __getitem__(self, key: int) -> bool:
        return key in self._pressed


@pytest.fixture(scope="session")
def pygame_env() -> Generator[Any, Any, Any]:
    pygame.init()
    pygame.display.set_mode((800, 400))
    yield
    pygame.quit()


@pytest.fixture
def default_config() -> DefaultConfig:
    return DefaultConfig()


@pytest.fixture
def player(pygame_env: Generator[Any, Any, Any]) -> PlayerModel:
    return PlayerModel()


@pytest.fixture
def interface_game(default_config: DefaultConfig) -> InterfaceGame:
    return InterfaceGame(config=default_config)


@pytest.fixture
def mock_keys() -> type[MockKeys]:
    return MockKeys
