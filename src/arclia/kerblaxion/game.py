
import sys

from dataclasses import dataclass, field

import pygame
from pygame.locals import *

from .hero import Hero

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

    self.visible_sprites.add(Hero(self))


  def run(self):
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
