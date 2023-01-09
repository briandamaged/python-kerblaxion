
from importlib import resources

from arclia.happygame.assets import (
  CachingAssetLoader,
  SoundLoader,
  SurfaceLoader,
)

_assets = resources.files(__name__)

load_surface = SurfaceLoader(_assets.joinpath("graphics"))
get_surface = CachingAssetLoader(load_surface)

load_sound = SoundLoader(_assets.joinpath("sfx"))
get_sound = CachingAssetLoader(load_sound)
