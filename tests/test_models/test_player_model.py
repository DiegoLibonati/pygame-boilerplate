from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.models.player_model import PlayerModel


class MockKeys:
    def __init__(self, pressed: set[int] | None = None) -> None:
        self._pressed: set[int] = pressed or set()

    def __getitem__(self, key: int) -> bool:
        return key in self._pressed


@pytest.fixture
def player() -> Generator[PlayerModel, None, None]:
    real_surface: pygame.Surface = pygame.Surface((50, 50))
    mock_image: MagicMock = MagicMock()
    mock_image.convert_alpha.return_value = real_surface
    mock_sound: MagicMock = MagicMock()
    with (
        patch("pygame.image.load", return_value=mock_image),
        patch("pygame.mixer.Sound", return_value=mock_sound),
    ):
        yield PlayerModel()


class TestPlayerModelInit:
    @pytest.mark.unit
    def test_is_sprite_subclass(self, player: PlayerModel) -> None:
        assert isinstance(player, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_initial_walk_index(self, player: PlayerModel) -> None:
        assert player._walk_index == 0.0

    @pytest.mark.unit
    def test_initial_gravity(self, player: PlayerModel) -> None:
        assert player._gravity == 0.0

    @pytest.mark.unit
    def test_initial_position_bottom(self, player: PlayerModel) -> None:
        assert player.rect.bottom == 300

    @pytest.mark.unit
    def test_initial_position_centerx(self, player: PlayerModel) -> None:
        assert player.rect.centerx == 80

    @pytest.mark.unit
    def test_walk_frames_count(self, player: PlayerModel) -> None:
        assert len(player._walk_frames) == 2

    @pytest.mark.unit
    def test_image_is_surface(self, player: PlayerModel) -> None:
        assert isinstance(player.image, pygame.Surface)

    @pytest.mark.unit
    def test_rect_is_rect(self, player: PlayerModel) -> None:
        assert isinstance(player.rect, pygame.Rect)

    @pytest.mark.unit
    def test_image_is_first_walk_frame(self, player: PlayerModel) -> None:
        assert player.image is player._walk_frames[0]

    @pytest.mark.unit
    def test_jump_sound_volume_set(self, player: PlayerModel) -> None:
        player._jump_sound.set_volume.assert_called_once_with(0.2)


class TestPlayerModelProperties:
    @pytest.mark.unit
    def test_is_grounded_when_at_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = 300
        assert player.is_grounded is True

    @pytest.mark.unit
    def test_is_grounded_when_below_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = 310
        assert player.is_grounded is True

    @pytest.mark.unit
    def test_is_not_grounded_when_airborne(self, player: PlayerModel) -> None:
        player.rect.bottom = 200
        assert player.is_grounded is False

    @pytest.mark.unit
    def test_is_jumping_when_airborne(self, player: PlayerModel) -> None:
        player.rect.bottom = 200
        assert player.is_jumping is True

    @pytest.mark.unit
    def test_is_not_jumping_when_grounded(self, player: PlayerModel) -> None:
        player.rect.bottom = 300
        assert player.is_jumping is False


class TestPlayerModelGravity:
    @pytest.mark.unit
    def test_gravity_increments_when_airborne(self, player: PlayerModel) -> None:
        player.rect.bottom = 200
        player._gravity = 0.0
        player._apply_gravity()
        assert player._gravity == 1.0

    @pytest.mark.unit
    def test_gravity_moves_rect_down(self, player: PlayerModel) -> None:
        player.rect.bottom = 200
        player._gravity = 5.0
        player._apply_gravity()
        assert player.rect.bottom == 206

    @pytest.mark.unit
    def test_gravity_clamps_to_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = 295
        player._gravity = 20.0
        player._apply_gravity()
        assert player.rect.bottom == 300

    @pytest.mark.unit
    def test_gravity_resets_on_clamp(self, player: PlayerModel) -> None:
        player.rect.bottom = 295
        player._gravity = 20.0
        player._apply_gravity()
        assert player._gravity == 0.0

    @pytest.mark.unit
    def test_grounded_player_stays_grounded(self, player: PlayerModel) -> None:
        player.rect.bottom = 300
        player._gravity = 0.0
        player._apply_gravity()
        assert player.rect.bottom == 300


class TestPlayerModelInput:
    @pytest.mark.unit
    def test_jump_sets_negative_gravity(self, player: PlayerModel) -> None:
        player.rect.bottom = 300
        keys: MockKeys = MockKeys({pygame.K_SPACE})
        player._input(keys)
        assert player._gravity == -20

    @pytest.mark.unit
    def test_jump_plays_sound(self, player: PlayerModel) -> None:
        player.rect.bottom = 300
        keys: MockKeys = MockKeys({pygame.K_SPACE})
        player._input(keys)
        player._jump_sound.play.assert_called_once()

    @pytest.mark.unit
    def test_move_right_increments_x(self, player: PlayerModel) -> None:
        initial_x: int = player.rect.x
        keys: MockKeys = MockKeys({pygame.K_d})
        player._input(keys)
        assert player.rect.x == initial_x + 2

    @pytest.mark.unit
    def test_move_left_decrements_x(self, player: PlayerModel) -> None:
        initial_x: int = player.rect.x
        keys: MockKeys = MockKeys({pygame.K_a})
        player._input(keys)
        assert player.rect.x == initial_x - 2

    @pytest.mark.unit
    def test_no_jump_when_airborne(self, player: PlayerModel) -> None:
        player.rect.bottom = 200
        player._gravity = -10.0
        keys: MockKeys = MockKeys({pygame.K_SPACE})
        player._input(keys)
        assert player._gravity == -10.0

    @pytest.mark.unit
    def test_no_movement_with_no_keys(self, player: PlayerModel) -> None:
        initial_x: int = player.rect.x
        keys: MockKeys = MockKeys()
        player._input(keys)
        assert player.rect.x == initial_x


class TestPlayerModelAnimate:
    @pytest.mark.unit
    def test_animate_uses_jump_frame_when_airborne(self, player: PlayerModel) -> None:
        player.rect.bottom = 200
        keys: MockKeys = MockKeys()
        player._animate(keys)
        assert player.image is player._jump_frame

    @pytest.mark.unit
    def test_animate_uses_walk_frame_when_moving_right(self, player: PlayerModel) -> None:
        player.rect.bottom = 300
        keys: MockKeys = MockKeys({pygame.K_d})
        player._animate(keys)
        assert player.image in player._walk_frames

    @pytest.mark.unit
    def test_animate_uses_walk_frame_when_moving_left(self, player: PlayerModel) -> None:
        player.rect.bottom = 300
        keys: MockKeys = MockKeys({pygame.K_a})
        player._animate(keys)
        assert player.image in player._walk_frames

    @pytest.mark.unit
    def test_animate_resets_walk_index_when_idle(self, player: PlayerModel) -> None:
        player.rect.bottom = 300
        player._walk_index = 0.5
        keys: MockKeys = MockKeys()
        player._animate(keys)
        assert player._walk_index == 0.0

    @pytest.mark.unit
    def test_animate_uses_first_frame_when_idle(self, player: PlayerModel) -> None:
        player.rect.bottom = 300
        keys: MockKeys = MockKeys()
        player._animate(keys)
        assert player.image is player._walk_frames[0]

    @pytest.mark.unit
    def test_animate_advances_walk_index_when_moving(self, player: PlayerModel) -> None:
        player.rect.bottom = 300
        player._walk_index = 0.0
        keys: MockKeys = MockKeys({pygame.K_d})
        player._animate(keys)
        assert player._walk_index > 0.0


class TestPlayerModelClampPosition:
    @pytest.mark.unit
    def test_clamp_below_left_boundary(self, player: PlayerModel) -> None:
        player.rect.x = -50
        player._clamp_position()
        assert player.rect.x == 0

    @pytest.mark.unit
    def test_clamp_above_right_boundary(self, player: PlayerModel) -> None:
        player.rect.x = 800
        player._clamp_position()
        assert player.rect.x == 735

    @pytest.mark.unit
    def test_no_clamp_within_bounds(self, player: PlayerModel) -> None:
        player.rect.x = 100
        player._clamp_position()
        assert player.rect.x == 100

    @pytest.mark.unit
    def test_clamp_at_left_boundary(self, player: PlayerModel) -> None:
        player.rect.x = 0
        player._clamp_position()
        assert player.rect.x == 0

    @pytest.mark.unit
    def test_clamp_at_right_boundary(self, player: PlayerModel) -> None:
        player.rect.x = 735
        player._clamp_position()
        assert player.rect.x == 735


class TestPlayerModelUpdate:
    @pytest.mark.unit
    def test_update_runs_without_error(self, player: PlayerModel) -> None:
        with patch("pygame.key.get_pressed", return_value=MockKeys()):
            player.update()

    @pytest.mark.unit
    def test_update_keeps_grounded_player_at_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = 300
        with patch("pygame.key.get_pressed", return_value=MockKeys()):
            player.update()
        assert player.rect.bottom == 300

    @pytest.mark.unit
    def test_update_clamps_x_from_negative(self, player: PlayerModel) -> None:
        player.rect.x = -100
        with patch("pygame.key.get_pressed", return_value=MockKeys()):
            player.update()
        assert player.rect.x >= 0

    @pytest.mark.unit
    def test_update_clamps_x_from_overflow(self, player: PlayerModel) -> None:
        player.rect.x = 900
        with patch("pygame.key.get_pressed", return_value=MockKeys()):
            player.update()
        assert player.rect.x <= 735
