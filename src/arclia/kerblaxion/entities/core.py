
class UpdateContext:
  def __init__(
    self,
    t_ms: int,
    dt_ms: int,
    game, # FIXME: Extract this
  ):
    self.t_ms = t_ms
    self.dt_ms = dt_ms

    self.t = t_ms / 1000
    self.dt = dt_ms / 1000

    self.game = game
