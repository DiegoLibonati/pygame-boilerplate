import sys

import pygame

from src.configs.default_config import DefaultConfig
from src.constants.paths import FONT_PRIMARY, GRAPHIC_GROUND, GRAPHIC_PLAYER_STAND, GRAPHIC_SKY, SOUND_MUSIC
from src.models.player_model import PlayerModel

_SCREEN_W = 800
_SCREEN_H = 400
_GROUND_Y = 300
_FPS = 60
_FONT_SIZE = 50
_MUSIC_VOLUME = 0.1
_COLOR_BG = (94, 129, 162)
_COLOR_TEXT = (111, 196, 169)


class InterfaceGame:
    TITLE = "Template Pygame"

    def __init__(self, config: DefaultConfig) -> None:
        pygame.init()

        self._config = config
        self._game_started: bool = False

        pygame.display.set_caption(self.TITLE)
        self._screen = pygame.display.set_mode((_SCREEN_W, _SCREEN_H))
        self._clock = pygame.time.Clock()
        self._player_single_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()

        self._load_assets()
        self._build_surfaces()
        self._setup()

    # --- Properties ---

    @property
    def screen(self) -> pygame.Surface:
        return self._screen

    @property
    def game_started(self) -> bool:
        return self._game_started

    @property
    def config(self) -> DefaultConfig:
        return self._config

    @property
    def player_single_group(self) -> pygame.sprite.GroupSingle:
        return self._player_single_group

    @property
    def player(self) -> PlayerModel | None:
        sprites = self._player_single_group.sprites()
        return sprites[0] if sprites else None

    @property
    def clock(self) -> pygame.time.Clock:
        return self._clock

    # --- Init helpers ---

    def _load_assets(self) -> None:
        self._bg_music = pygame.mixer.Sound(SOUND_MUSIC)
        self._primary_font = pygame.font.Font(FONT_PRIMARY, _FONT_SIZE)
        self._sky_surface = pygame.image.load(GRAPHIC_SKY).convert()
        self._ground_surface = pygame.image.load(GRAPHIC_GROUND).convert()
        self._player_stand_surface = pygame.transform.scale2x(pygame.image.load(GRAPHIC_PLAYER_STAND).convert_alpha())

    def _build_surfaces(self) -> None:
        self._player_stand_rect = self._player_stand_surface.get_rect(center=(_SCREEN_W // 2, _SCREEN_H // 2))
        self._press_space_surface = self._primary_font.render("Press Space to Start", False, _COLOR_TEXT)
        self._press_space_rect = self._press_space_surface.get_rect(center=(_SCREEN_W // 2, 340))

    def _setup(self) -> None:
        self._bg_music.set_volume(_MUSIC_VOLUME)
        self._player_single_group.add(PlayerModel())

    # --- Game loop ---

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not self._game_started and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._game_started = True
                self._bg_music.play(loops=-1)

    def _render_intro(self) -> None:
        self._screen.fill(_COLOR_BG)
        self._screen.blit(self._player_stand_surface, self._player_stand_rect)
        self._screen.blit(self._press_space_surface, self._press_space_rect)

    def _render_game(self) -> None:
        self._screen.blit(self._sky_surface, (0, 0))
        self._screen.blit(self._ground_surface, (0, _GROUND_Y))
        self._player_single_group.draw(surface=self._screen)
        self._player_single_group.update()

    def game_loop(self) -> None:
        while True:
            self._handle_events()

            if self._game_started:
                self._render_game()
            else:
                self._render_intro()

            pygame.display.update()
            self._clock.tick(_FPS)
