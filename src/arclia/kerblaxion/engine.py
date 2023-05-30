
from dataclasses import dataclass

from pygame import Vector2
from arclia.happygame.math import Vector2Coercible

from .moment import Moment, Ticker

@dataclass
class UpdateContext:
  now: Moment

  def scale(self, v: Vector2Coercible):
    return Vector2(v) * self.now.dt
