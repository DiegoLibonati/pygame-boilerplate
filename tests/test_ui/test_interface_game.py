from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.configs.default_config import DefaultConfig
from src.models.player_model import PlayerModel
from src.ui.interface_game import InterfaceGame


@pytest.fixture
def mock_assets() -> Generator[None, None, None]:
    real_surface: pygame.Surface = pygame.Surface((50, 50))
    mock_image: MagicMock = MagicMock()
    mock_image.convert.return_value = real_surface
    mock_image.convert_alpha.return_value = real_surface
    mock_sound_instance: MagicMock = MagicMock()
    mock_font_instance: MagicMock = MagicMock()
    mock_font_instance.render.return_value = real_surface
    with (
        patch("pygame.image.load", return_value=mock_image),
        patch("pygame.mixer.Sound", return_value=mock_sound_instance),
        patch("pygame.font.Font", return_value=mock_font_instance),
        patch("pygame.transform.scale2x", return_value=real_surface),
    ):
        yield


@pytest.fixture
def interface(mock_assets: None) -> InterfaceGame:
    return InterfaceGame(DefaultConfig())


class TestInterfaceGameTitle:
    @pytest.mark.unit
    def test_title_is_string(self) -> None:
        assert isinstance(InterfaceGame.TITLE, str)

    @pytest.mark.unit
    def test_title_value(self) -> None:
        assert InterfaceGame.TITLE == "Python Pygame Boilerplate"


class TestInterfaceGameInit:
    @pytest.mark.unit
    def test_initial_game_started_is_false(self, interface: InterfaceGame) -> None:
        assert interface.game_started is False

    @pytest.mark.unit
    def test_config_is_stored(self, interface: InterfaceGame) -> None:
        assert isinstance(interface.config, DefaultConfig)

    @pytest.mark.unit
    def test_screen_is_surface(self, interface: InterfaceGame) -> None:
        assert isinstance(interface.screen, pygame.Surface)

    @pytest.mark.unit
    def test_screen_width(self, interface: InterfaceGame) -> None:
        assert interface.screen.get_width() == 800

    @pytest.mark.unit
    def test_screen_height(self, interface: InterfaceGame) -> None:
        assert interface.screen.get_height() == 400

    @pytest.mark.unit
    def test_clock_is_clock(self, interface: InterfaceGame) -> None:
        assert isinstance(interface.clock, pygame.time.Clock)

    @pytest.mark.unit
    def test_player_group_is_group_single(self, interface: InterfaceGame) -> None:
        assert isinstance(interface.player_single_group, pygame.sprite.GroupSingle)


class TestInterfaceGameProperties:
    @pytest.mark.unit
    def test_game_started_property_is_false(self, interface: InterfaceGame) -> None:
        assert interface.game_started is False

    @pytest.mark.unit
    def test_player_property_returns_player_model(self, interface: InterfaceGame) -> None:
        assert isinstance(interface.player, PlayerModel)

    @pytest.mark.unit
    def test_player_property_returns_none_when_group_empty(self, interface: InterfaceGame) -> None:
        interface.player_single_group.empty()
        assert interface.player is None

    @pytest.mark.unit
    def test_config_property_returns_config(self, interface: InterfaceGame) -> None:
        config: DefaultConfig = interface.config
        assert isinstance(config, DefaultConfig)

    @pytest.mark.unit
    def test_screen_property_returns_surface(self, interface: InterfaceGame) -> None:
        assert isinstance(interface.screen, pygame.Surface)

    @pytest.mark.unit
    def test_clock_property_returns_clock(self, interface: InterfaceGame) -> None:
        assert isinstance(interface.clock, pygame.time.Clock)

    @pytest.mark.unit
    def test_player_single_group_property(self, interface: InterfaceGame) -> None:
        assert isinstance(interface.player_single_group, pygame.sprite.GroupSingle)


class TestInterfaceGameHandleEvents:
    @pytest.mark.unit
    def test_space_keydown_starts_game(self, interface: InterfaceGame) -> None:
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        with patch("pygame.event.get", return_value=[event]):
            interface._handle_events()
        assert interface.game_started is True

    @pytest.mark.unit
    def test_space_key_ignored_when_game_already_started(self, interface: InterfaceGame) -> None:
        interface._game_started = True
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        with patch("pygame.event.get", return_value=[event]):
            interface._handle_events()
        assert interface.game_started is True

    @pytest.mark.unit
    def test_quit_event_calls_sys_exit(self, interface: InterfaceGame) -> None:
        quit_event: pygame.event.Event = pygame.event.Event(pygame.QUIT)
        with (
            patch("pygame.event.get", return_value=[quit_event]),
            patch("sys.exit") as mock_exit,
            patch("pygame.quit"),
        ):
            interface._handle_events()
        mock_exit.assert_called_once()

    @pytest.mark.unit
    def test_no_events_does_not_change_state(self, interface: InterfaceGame) -> None:
        with patch("pygame.event.get", return_value=[]):
            interface._handle_events()
        assert interface.game_started is False

    @pytest.mark.unit
    def test_space_starts_music(self, interface: InterfaceGame) -> None:
        event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        with patch("pygame.event.get", return_value=[event]):
            interface._handle_events()
        interface._bg_music.play.assert_called_once_with(loops=-1)
