
import sys

import pygame
from pygame.locals import *


class Game(object):
  def __init__(self):
    pygame.display.init()
    pygame.font.init()

    self.display_surface = pygame.display.set_mode(
      size = (1280, 720),
    )

    pygame.display.set_caption("spaXion")

    self.clock = pygame.time.Clock()
    self.fps = 30

    self.visible_sprites = pygame.sprite.LayeredDirty()


  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()

      self.display_surface.fill(color = (0, 0, 0))

      pygame.display.update()

      self.clock.tick(self.fps)
