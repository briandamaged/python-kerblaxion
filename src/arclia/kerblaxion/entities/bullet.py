
from dataclasses import dataclass

import pygame
from pygame.sprite import Group
from pygame.math import Vector2

from arclia.happygame.math import Vector2Coercible

from ..engine import UpdateContext


@dataclass
class BulletFactory(object):
  visible_sprites: Group
  enemies: Group

  def create(self, *args, **kwargs):
    b = Bullet(*args, **kwargs, enemies = self.enemies)
    self.visible_sprites.add(b)
    return b


class Bullet(pygame.sprite.Sprite):
  def __init__(
    self,
    position: Vector2Coercible,
    velocity: Vector2Coercible,
    enemies: Group,
  ):
    super().__init__()
    self.position = Vector2(position)
    self.velocity = Vector2(velocity)

    self.image = pygame.surface.Surface(size = (4, 4))
    self.image.fill(color = (255, 255, 0))

    self.enemies = enemies

  @property
  def rect(self):
    return self.image.get_rect(
      center = self.position,
    )

  def update(self, ctx: UpdateContext):
    self.position += ctx.scale(self.velocity)

    # TODO: Extract collision behavior
    collisions = pygame.sprite.spritecollide(
      sprite = self,
      group = self.enemies,
      dokill = False,
    )

    if len(collisions) > 0:
      for c in collisions:
        c.destroy()
      self.kill()
      return

    if self.rect.bottom < 0:
      self.kill()

