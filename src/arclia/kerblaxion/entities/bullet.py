
import pygame
from pygame.math import Vector2

from arclia.happygame.math import Vector2Coercible

from .core import UpdateContext


class BulletFactory(object):
  def __init__(self):
    pass

  def create(self):
    pass


class Bullet(pygame.sprite.Sprite):
  def __init__(
    self,
    position: Vector2Coercible,
    velocity: Vector2Coercible,
  ):
    super().__init__()
    self.position = Vector2(position)
    self.velocity = Vector2(velocity)

    self.image = pygame.surface.Surface(size = (4, 4))
    self.image.fill(color = (255, 255, 0))

  @property
  def rect(self):
    return self.image.get_rect(
      center = self.position,
    )

  def update(self, ctx: UpdateContext):
    self.position += self.velocity * ctx.dt

    # TODO: Extract collision behavior
    collisions = pygame.sprite.spritecollide(
      sprite = self,
      group = ctx.game.enemies,
      dokill = False,
    )

    if len(collisions) > 0:
      for c in collisions:
        c.destroy()
      self.kill()
      return

    if self.rect.bottom < 0:
      self.kill()

