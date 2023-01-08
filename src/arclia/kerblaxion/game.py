
import sys

from dataclasses import dataclass, field

import pygame
from pygame.locals import *

from .hero import Hero



class Enemy(pygame.sprite.Sprite):
  def __init__(self, position):
    super().__init__()

    self.image = pygame.surface.Surface(
      size = (64, 64),
    )

    self.image.fill(color = (255, 0, 0))

    self.rect = self.image.get_rect(
      center = position,
    )




@dataclass(frozen = True)
class Instant:
  t: int
  dt: int

class Game(object):
  def __init__(self):
    pygame.display.init()
    pygame.mixer.init()
    # pygame.font.init()

    self.display_surface = pygame.display.set_mode(
      size = (1280, 720),
    )

    pygame.display.set_caption("kerblaxion")

    self.clock = pygame.time.Clock()
    self.fps = 30

    self.visible_sprites = pygame.sprite.Group()
    self.player_bullets = pygame.sprite.Group()
    self.enemies = pygame.sprite.Group()

    self.visible_sprites.add(Hero(
      position = (1280 / 2, 640),
      game = self,
    ))

    for x in range(100, 1000, 96):
      for y in range(100, 300, 96):
        e = Enemy(position = (x, y))
        self.visible_sprites.add(e)
        self.enemies.add(e)



  def run(self):
    pygame.mixer.music.load("arclia/kerblaxion/assets/music/level01.mp3")
    pygame.mixer.music.play(-1)
    while True:
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()

      self.visible_sprites.update()

      self.display_surface.fill(color = (0, 0, 0))
      self.visible_sprites.draw(self.display_surface)

      pygame.display.update()

      self.clock.tick(self.fps)
