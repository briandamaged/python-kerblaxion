
from importlib import resources

import pygame
from pygame.locals import *

from arclia.pubsub import Publisher


class Bullet(pygame.sprite.Sprite):
  def __init__(self, position):
    super().__init__()
    self.image = pygame.surface.Surface(size = (16, 16))
    self.image.fill(color = (255, 255, 0))

    self.rect = self.image.get_rect(
      center = position,
    )

  def update(self):
    self.rect.y -= 16

    if self.rect.bottom < 0:
      print("BOOM!")
      self.kill()


class Hero(pygame.sprite.Sprite):
  def __init__(self, game):
    super().__init__()
    self.game = game

    with resources.open_binary("arclia.kerblaxion", "hero.png") as fin:
      self.image = pygame.image.load(fin)

    self.rect = self.image.get_rect(
      center = (500, 500),
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
          Bullet(position = self.rect.center)
        )
        self.shoot_sfx.play()
        self.shooting = True
    else:
      self.shooting = False

