import os

import pygame
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


@pytest.fixture(scope="session", autouse=True)
def pygame_init() -> None:
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture(scope="session")
def surface() -> pygame.Surface:
    return pygame.display.set_mode((800, 600))
