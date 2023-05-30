
import pygame

from arclia.pubsub import Publisher

class Moment:
  def __init__(self, t_ms: int, dt_ms: int):
    self.t_ms = t_ms
    self.dt_ms = dt_ms

    self.t = t_ms / 1000
    self.dt = dt_ms / 1000


class Engine:
  def __init__(self):
    self.now = Moment(
      t_ms = 0,
      dt_ms = 0,
    )

    self.on_tick, self._emit_tick = Publisher[Engine].methods()

  def tick(self):
    t = pygame.time.get_ticks()
    self.now = Moment(
      t_ms = t,
      dt_ms = (t - self.now.t_ms),
    )

    self._emit_tick(self)

  def mainloop(self):
    while True:
      self.tick()
