
import pygame
from pygame.locals import *

from ..assets import get_surface, get_sound

from .core import UpdateContext
from .bullet import Bullet

class Hero(pygame.sprite.Sprite):
  def __init__(self, position):
    super().__init__()

    self.images = [
      get_surface(f"hero/hero0{i + 1}.png")
      for i in range(4)
    ]

    self.image_index = 0

    self.rect = self.image.get_rect(
      center = position,
    )

    self.shoot_sfx = get_sound("shoot.wav")

    self.shooting = False

  @property
  def image(self):
    return self.images[self.image_index]

  def update(self, ctx: UpdateContext):
    self.image_index = (ctx.t_ms >> 5) % 4

    pressed = pygame.key.get_pressed()
    boosted = pressed[K_LSHIFT]

    v = 25 * (3 if boosted else 2) * ctx.dt

    if pressed[K_LEFT]:
      self.rect.x -= v

    if pressed[K_RIGHT]:
      self.rect.x += v

    if pressed[K_SPACE]:
      if not self.shooting:
        ctx.game.visible_sprites.add(
          Bullet(
            position = self.rect.center,
            velocity = (0, -75),
          )
        )
        self.shoot_sfx.play()
        self.shooting = True
    else:
      self.shooting = False

