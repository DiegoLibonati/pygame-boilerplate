import os

import pytest

from src.constants.paths import (
    FONT_PRIMARY,
    GRAPHIC_GROUND,
    GRAPHIC_PLAYER_JUMP,
    GRAPHIC_PLAYER_STAND,
    GRAPHIC_PLAYER_WALK_1,
    GRAPHIC_PLAYER_WALK_2,
    GRAPHIC_SKY,
    SOUND_MUSIC,
    SOUND_PLAYER_JUMP,
)


class TestPathTypes:
    @pytest.mark.unit
    def test_sound_music_is_string(self) -> None:
        assert isinstance(SOUND_MUSIC, str)

    @pytest.mark.unit
    def test_sound_player_jump_is_string(self) -> None:
        assert isinstance(SOUND_PLAYER_JUMP, str)

    @pytest.mark.unit
    def test_font_primary_is_string(self) -> None:
        assert isinstance(FONT_PRIMARY, str)

    @pytest.mark.unit
    def test_graphic_sky_is_string(self) -> None:
        assert isinstance(GRAPHIC_SKY, str)

    @pytest.mark.unit
    def test_graphic_ground_is_string(self) -> None:
        assert isinstance(GRAPHIC_GROUND, str)

    @pytest.mark.unit
    def test_graphic_player_stand_is_string(self) -> None:
        assert isinstance(GRAPHIC_PLAYER_STAND, str)

    @pytest.mark.unit
    def test_graphic_player_walk_1_is_string(self) -> None:
        assert isinstance(GRAPHIC_PLAYER_WALK_1, str)

    @pytest.mark.unit
    def test_graphic_player_walk_2_is_string(self) -> None:
        assert isinstance(GRAPHIC_PLAYER_WALK_2, str)

    @pytest.mark.unit
    def test_graphic_player_jump_is_string(self) -> None:
        assert isinstance(GRAPHIC_PLAYER_JUMP, str)


class TestPathValues:
    @pytest.mark.unit
    def test_all_paths_are_nonempty(self) -> None:
        paths: list[str] = [
            SOUND_MUSIC,
            SOUND_PLAYER_JUMP,
            FONT_PRIMARY,
            GRAPHIC_SKY,
            GRAPHIC_GROUND,
            GRAPHIC_PLAYER_STAND,
            GRAPHIC_PLAYER_WALK_1,
            GRAPHIC_PLAYER_WALK_2,
            GRAPHIC_PLAYER_JUMP,
        ]
        for path in paths:
            assert path != ""

    @pytest.mark.unit
    def test_all_paths_are_absolute(self) -> None:
        paths: list[str] = [
            SOUND_MUSIC,
            SOUND_PLAYER_JUMP,
            FONT_PRIMARY,
            GRAPHIC_SKY,
            GRAPHIC_GROUND,
            GRAPHIC_PLAYER_STAND,
            GRAPHIC_PLAYER_WALK_1,
            GRAPHIC_PLAYER_WALK_2,
            GRAPHIC_PLAYER_JUMP,
        ]
        for path in paths:
            assert os.path.isabs(path)

    @pytest.mark.unit
    def test_sound_music_filename(self) -> None:
        assert SOUND_MUSIC.endswith("game_music.wav")

    @pytest.mark.unit
    def test_sound_player_jump_filename(self) -> None:
        assert SOUND_PLAYER_JUMP.endswith("player_jump.mp3")

    @pytest.mark.unit
    def test_font_primary_filename(self) -> None:
        assert FONT_PRIMARY.endswith("Pixeltype.ttf")

    @pytest.mark.unit
    def test_graphic_sky_filename(self) -> None:
        assert GRAPHIC_SKY.endswith("sky.png")

    @pytest.mark.unit
    def test_graphic_ground_filename(self) -> None:
        assert GRAPHIC_GROUND.endswith("ground.png")

    @pytest.mark.unit
    def test_graphic_player_stand_filename(self) -> None:
        assert GRAPHIC_PLAYER_STAND.endswith("player_stand.png")

    @pytest.mark.unit
    def test_graphic_player_walk_1_filename(self) -> None:
        assert GRAPHIC_PLAYER_WALK_1.endswith("player_walk_1.png")

    @pytest.mark.unit
    def test_graphic_player_walk_2_filename(self) -> None:
        assert GRAPHIC_PLAYER_WALK_2.endswith("player_walk_2.png")

    @pytest.mark.unit
    def test_graphic_player_jump_filename(self) -> None:
        assert GRAPHIC_PLAYER_JUMP.endswith("player_jump.png")

    @pytest.mark.unit
    def test_paths_contain_assets_segment(self) -> None:
        paths: list[str] = [
            SOUND_MUSIC,
            SOUND_PLAYER_JUMP,
            FONT_PRIMARY,
            GRAPHIC_SKY,
            GRAPHIC_GROUND,
            GRAPHIC_PLAYER_STAND,
            GRAPHIC_PLAYER_WALK_1,
            GRAPHIC_PLAYER_WALK_2,
            GRAPHIC_PLAYER_JUMP,
        ]
        for path in paths:
            assert "assets" in path
