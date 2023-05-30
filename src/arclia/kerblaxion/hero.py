
import random
import pygame
from pygame.locals import *


from .assets import get_sound
from .ui.score import Scoreboard
from .game import Scene

from .engine import UpdateContext
from .entities.bullet import BulletFactory
from .entities.invader import Enemy, EnemyFactory
from .entities.hero import Hero
from .entities.star import Star




class GameScene(Scene):
  def __init__(self):
    self.background_sprites = pygame.sprite.Group()
    self.visible_sprites = pygame.sprite.Group()
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

  def handle_enemy_destroyed(enemy: Enemy):
    scene.scoreboard.score += 250

  scene.visible_sprites.add(Hero(
    position = (180, 160),
    bullet_factory = BulletFactory(
      visible_sprites = scene.visible_sprites,
      enemies = scene.enemies,
    ),
  ))

  enemy_factory = EnemyFactory(
    visible_sprites = scene.visible_sprites,
    enemies = scene.enemies,
  )

  for x in range(16, 260, 24):
    for y in range(16, 100, 24):
      e = enemy_factory.create(
        position = (x, y),
      )

      e.on_destroyed(handle_enemy_destroyed)

  return scene
