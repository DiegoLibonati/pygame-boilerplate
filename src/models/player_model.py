import pygame

from src.constants.paths import GRAPHIC_PLAYER_JUMP, GRAPHIC_PLAYER_WALK_1, GRAPHIC_PLAYER_WALK_2, SOUND_PLAYER_JUMP

_GROUND_Y = 300
_SPAWN_X = 80
_JUMP_VELOCITY = -20
_GRAVITY = 1
_MOVE_SPEED = 2
_WALK_ANIM_SPEED = 0.1
_LEFT_BOUNDARY = 0
_RIGHT_BOUNDARY = 735
_JUMP_VOLUME = 0.2


class PlayerModel(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self._walk_index: float = 0.0
        self._gravity: float = 0.0

        self._walk_frames: list[pygame.Surface] = [
            pygame.image.load(GRAPHIC_PLAYER_WALK_1).convert_alpha(),
            pygame.image.load(GRAPHIC_PLAYER_WALK_2).convert_alpha(),
        ]
        self._jump_frame: pygame.Surface = pygame.image.load(GRAPHIC_PLAYER_JUMP).convert_alpha()
        self._jump_sound: pygame.mixer.Sound = pygame.mixer.Sound(SOUND_PLAYER_JUMP)

        self.image: pygame.Surface = self._walk_frames[0]
        self.rect: pygame.Rect = self.image.get_rect(midbottom=(_SPAWN_X, _GROUND_Y))

        self._setup()

    # --- Properties ---

    @property
    def is_grounded(self) -> bool:
        return self.rect.bottom >= _GROUND_Y

    @property
    def is_jumping(self) -> bool:
        return not self.is_grounded

    # --- Init helpers ---

    def _setup(self) -> None:
        self._jump_sound.set_volume(_JUMP_VOLUME)

    # --- Update steps ---

    def _input(self, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_SPACE] and self.is_grounded:
            self._jump_sound.play()
            self._gravity = _JUMP_VELOCITY
        elif keys[pygame.K_d]:
            self.rect.x += _MOVE_SPEED
        elif keys[pygame.K_a]:
            self.rect.x -= _MOVE_SPEED

    def _apply_gravity(self) -> None:
        self._gravity += _GRAVITY
        self.rect.y += self._gravity

        if self.rect.bottom >= _GROUND_Y:
            self.rect.bottom = _GROUND_Y
            self._gravity = 0

    def _animate(self, keys: pygame.key.ScancodeWrapper) -> None:
        if self.is_jumping:
            self.image = self._jump_frame
            return

        moving = keys[pygame.K_a] or keys[pygame.K_d]

        if moving:
            self._walk_index = (self._walk_index + _WALK_ANIM_SPEED) % len(self._walk_frames)
            self.image = self._walk_frames[int(self._walk_index)]
        else:
            self._walk_index = 0.0
            self.image = self._walk_frames[0]

    def _clamp_position(self) -> None:
        self.rect.x = max(_LEFT_BOUNDARY, min(self.rect.x, _RIGHT_BOUNDARY))

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        self._input(keys)
        self._apply_gravity()
        self._animate(keys)
        self._clamp_position()
