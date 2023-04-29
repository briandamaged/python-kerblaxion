
import random
import pygame
from pygame.locals import *

from arclia.happygame.math import Vector2Coercible
from arclia.pubsub import Publisher

from .assets import get_surface, get_sound
from .ui.score import Scoreboard
from .game import Scene

from .entities.core import UpdateContext
from .entities.hero import Hero

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
    c = (distance * 32) + 1
    self.image.fill(
      color = (c, c, c),
    )

  @property
  def rect(self):
    return self.image.get_rect(center = self.position)

  def update(self, ctx: UpdateContext):
    self.position.y += self.speed
    if self.rect.top > 180:
      self.kill()


class Explosion(pygame.sprite.Sprite):
  def __init__(self,
    position: Vector2Coercible,
  ):
    super().__init__()
    self.position = pygame.Vector2(position)

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
    self.explode_index = (ctx.t_ms - self.started_at) >> 5

    if self.explode_index >= len(self.explosions):
      self.kill()


class Enemy(pygame.sprite.Sprite):
  def __init__(self,
    position: Vector2Coercible,
  ):
    super().__init__()
    self.position = pygame.Vector2(position)

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
    self.position.x += (self.direction)

    r = self.rect
    if r.right >= 320 or r.left <= 0:
      self.direction = -self.direction
      self.position.x += (self.direction)
      self.position.y += 8

class GameScene(Scene):
  def __init__(self):
    self.background_sprites = pygame.sprite.Group()
    self.visible_sprites = pygame.sprite.Group()
    self.player_bullets = pygame.sprite.Group()
    self.enemies = pygame.sprite.Group()

    self.scoreboard = Scoreboard()

    for y in range(0, 180):
      self._generate_stars(y)

  def _generate_stars(self, y: float = 0.0):
    for _ in range(random.randint(0, 2)):
      star = Star(
        position = (random.random() * 320, y),
      )

      self.background_sprites.add(star)

  def update(self, ctx: UpdateContext):
    self._generate_stars()
    self.background_sprites.update(ctx)
    self.visible_sprites.update(ctx)

  def draw(self, surface: pygame.surface.Surface):
    surface.fill(color = (0, 0, 0))
    self.background_sprites.draw(surface)
    self.visible_sprites.draw(surface)

    surface.blit(
      self.scoreboard.image,
      dest = self.scoreboard.image.get_rect(
        topright = (320, 0),
      )
    )


def prepare():
  scene = GameScene()

  explode_sfx = get_sound("hero-explode.wav")

  def handle_enemy_destroyed(enemy: Enemy):
    scene.scoreboard.score += 250
    explosion = Explosion(position = enemy.position)
    scene.visible_sprites.add(explosion)
    explode_sfx.play()

  scene.visible_sprites.add(Hero(
    position = (180, 160),
  ))

  for x in range(16, 260, 24):
    for y in range(16, 100, 24):
      e = Enemy(
        position = (x, y),
      )

      e.on_destroyed(handle_enemy_destroyed)

      scene.visible_sprites.add(e)
      scene.enemies.add(e)

  return scene
