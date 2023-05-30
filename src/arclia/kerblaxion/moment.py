
from typing import Optional

import pygame

class Moment:
  def __init__(self, t_ms: int, dt_ms: int):
    self.t_ms = t_ms
    self.dt_ms = dt_ms

    self.t = self.t_ms / 1000
    self.dt = self.dt_ms / 1000

class Ticker:
  def __init__(self, t_ms: Optional[int] = None):
    self.t_ms = pygame.time.get_ticks() if t_ms is None else t_ms

  def tick(self):
    t_ms = pygame.time.get_ticks()

    m = Moment(
      t_ms = t_ms,
      dt_ms = (t_ms - self.t_ms),
    )

    self.t_ms = t_ms

    return m
