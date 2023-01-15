
import logging

from enum import Enum
from contextlib import contextmanager

from dataclasses import dataclass

import pygame
from pygame.locals import *

from arclia.pubsub import Publisher

from .assets import MUSIC_PATH
from .ui.score import Scoreboard

LOGGER = logging.getLogger(__name__)

@contextmanager
def pygame_session():
  pygame.display.init()
  pygame.mixer.init()
  pygame.font.init()  

  yield

  pygame.quit()



@dataclass(frozen = True)
class Instant:
  t: int
  dt: int



class ExecutionState(Enum):
  STOPPED = 0
  STARTING = 1
  RUNNING = 2
  STOPPING = 3


class GameManager(object):
  def __init__(self,
    scale: int = 4,
    fps: int = 30,
  ):
    self._render_surface = pygame.surface.Surface(
      size = (320, 180),
    )

    self._display_surface = pygame.display.set_mode(
      size = (
        self._render_surface.get_width() * scale,
        self._render_surface.get_height() * scale,
      ),
    )

    pygame.display.set_caption("KERBLAXION")

    self.clock = pygame.time.Clock()
    self.fps = fps

    self.visible_sprites = pygame.sprite.Group()
    self.player_bullets = pygame.sprite.Group()
    self.enemies = pygame.sprite.Group()

    self.event_received = Publisher[pygame.event.Event]()

    self.execution_state = ExecutionState.STOPPED

    self.scoreboard = Scoreboard()

  def request_shutdown(self):
    if self.execution_state == ExecutionState.RUNNING:
      self.execution_state = ExecutionState.STOPPING
    else:
      LOGGER.warn(f"Shutdown was requested while {type(self)} was in {self.execution_state} state")

  def run(self):
    if self.execution_state != ExecutionState.STOPPED:
      raise ValueError(f"`run()` cannot be invoked unless the {type(self)} is in the {ExecutionState.STOPPED} state")


    self.execution_state = ExecutionState.STARTING

    # TODO: Extract this logic
    pygame.mixer.music.load(MUSIC_PATH.joinpath("level01.mp3").open())
    pygame.mixer.music.play(-1)

    self.execution_state = ExecutionState.RUNNING
    while self.execution_state == ExecutionState.RUNNING:
      for event in pygame.event.get():
        self.event_received(event)

      self.visible_sprites.update()

      self._render_surface.fill(color = (0, 0, 0))
      self.visible_sprites.draw(self._render_surface)

      self._render_surface.blit(
        self.scoreboard.image,
        dest = self.scoreboard.image.get_rect(
          topright = (320, 0),
        )
      )

      pygame.transform.scale(
        surface = self._render_surface,
        size = (
          self._display_surface.get_width(),
          self._display_surface.get_height(),
        ),
        dest_surface = self._display_surface,
      )

      pygame.display.update()

      self.clock.tick(self.fps)

