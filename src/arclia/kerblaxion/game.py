
import sys

from dataclasses import dataclass

import pygame
from pygame.locals import *

from arclia.pubsub import Publisher

from .assets import MUSIC_PATH



@dataclass(frozen = True)
class Instant:
  t: int
  dt: int

class Game(object):
  def __init__(self):
    pygame.display.init()
    pygame.mixer.init()
    pygame.font.init()

    self.display_surface = pygame.display.set_mode(
      size = (1280, 720),
    )

    self.render_surface = pygame.surface.Surface(
      size = (320, 180),
    )

    pygame.display.set_caption("KERBLAXION")

    self.clock = pygame.time.Clock()
    self.fps = 30

    self.visible_sprites = pygame.sprite.Group()
    self.player_bullets = pygame.sprite.Group()
    self.enemies = pygame.sprite.Group()

    self.event_received = Publisher[pygame.event.Event]()

  def quit(self):
    pygame.quit()
    sys.exit()

  def run(self):
    pygame.mixer.music.load(MUSIC_PATH.joinpath("level01.mp3").open())
    pygame.mixer.music.play(-1)
    while True:
      for event in pygame.event.get():
        self.event_received(event)

      self.visible_sprites.update()

      self.render_surface.fill(color = (0, 0, 0))
      self.visible_sprites.draw(self.render_surface)

      pygame.transform.scale(
        surface = self.render_surface,
        size = (1280, 720),
        dest_surface = self.display_surface,
      )

      pygame.display.update()

      self.clock.tick(self.fps)



