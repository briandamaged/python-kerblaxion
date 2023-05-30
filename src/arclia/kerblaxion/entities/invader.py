
import pygame
from pygame import Vector2

from arclia.pubsub import Publisher
from arclia.happygame.math import Vector2Coercible

from ..assets import get_sound, get_surface

from ..engine import UpdateContext


class Explosion(pygame.sprite.Sprite):
  def __init__(self,
    position: Vector2Coercible,
  ):
    super().__init__()
    self.position = Vector2(position)

    self.explode_index = 0
    self.explosions = [
      get_surface(f"explode0{i+1}.png")
      for i in range(4)
    ]

    self.started_at = pygame.time.get_ticks()


  @property
  def image(self):
    return self.explosions[self.explode_index]

  @property
  def rect(self):
    return self.image.get_rect(
      center = self.position,
    )

  def update(self, ctx: UpdateContext):
    # Update the explosion animation every 32 milliseconds
    self.explode_index = (ctx.now.t_ms - self.started_at) >> 5

    if self.explode_index >= len(self.explosions):
      self.kill()


class Enemy(pygame.sprite.Sprite):
  def __init__(self,
    position: Vector2Coercible,
  ):
    super().__init__()
    self.position = Vector2(position)

    self.image = get_surface("enemy01.png")

    self.direction = +1

    [self.on_destroyed, self._emit_destroyed] = Publisher[Enemy].methods()

  @property
  def rect(self):
    return self.image.get_rect(
      center = self.position,
    )

  def destroy(self):
    self._emit_destroyed(self)
    self.kill()

  def update(self, ctx: UpdateContext):
    self.position.x += (self.direction) * 30 * ctx.now.dt

    r = self.rect
    if r.right >= 320 or r.left <= 0:
      self.direction = -self.direction
      self.position.x += (self.direction)
      self.position.y += 8
