
from importlib import resources

import pygame
from pygame.locals import *

from arclia.pubsub import Publisher


class Bullet(pygame.sprite.Sprite):
  def __init__(self, position, game):
    super().__init__()
    self.game = game

    self.image = pygame.surface.Surface(size = (16, 16))
    self.image.fill(color = (255, 255, 0))

    self.rect = self.image.get_rect(
      center = position,
    )

    self.explode_sfx = pygame.mixer.Sound("arclia/kerblaxion/assets/sfx/hero-explode.wav")

  def update(self):
    self.rect.y -= 16

    collisions = pygame.sprite.spritecollide(
      sprite = self,
      group = self.game.enemies,
      dokill = True,
    )

    if len(collisions) > 0:
      self.explode_sfx.play()
      self.kill()
      return

    if self.rect.bottom < 0:
      self.kill()


class Hero(pygame.sprite.Sprite):
  def __init__(self, position, game):
    super().__init__()
    self.game = game

    with resources.open_binary("arclia.kerblaxion", "hero.png") as fin:
      self.image = pygame.image.load(fin)

    self.rect = self.image.get_rect(
      center = position,
    )

    self.shoot_sfx = pygame.mixer.Sound("arclia/kerblaxion/assets/sfx/shoot.wav")

    self.shooting = False

  def update(self):
    pressed = pygame.key.get_pressed()
    boosted = pressed[K_LSHIFT]

    v = 8 * (2 if boosted else 1)

    if pressed[K_LEFT]:
      self.rect.x -= v

    if pressed[K_RIGHT]:
      self.rect.x += v

    if pressed[K_SPACE]:
      if not self.shooting:
        self.game.visible_sprites.add(
          Bullet(
            position = self.rect.center,
            game = self.game,
          )
        )
        self.shoot_sfx.play()
        self.shooting = True
    else:
      self.shooting = False

