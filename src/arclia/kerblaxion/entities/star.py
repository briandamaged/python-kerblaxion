
import random

import pygame

from arclia.happygame.math import Vector2Coercible

from ..engine import UpdateContext


class Star(pygame.sprite.Sprite):
  def __init__(self, position: Vector2Coercible):
    super().__init__()
    self.position = pygame.Vector2(position)

    size = random.randint(1, 2)
    self.image = pygame.surface.Surface(
      size = (size, size),
    )

    distance = random.random()
    self.speed = 0.5 + distance
    c = (distance * 64) + 1
    self.image.fill(
      color = (c, c, c),
    )

  @property
  def rect(self):
    return self.image.get_rect(center = self.position)

  def update(self, ctx: UpdateContext):
    # TODO: Fix this so that it takes ctx.dt into consideration
    self.position.y += self.speed

    if self.rect.top > 180:
      self.kill()
