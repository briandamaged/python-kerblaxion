
from importlib import resources

from arclia.happygame.assets import SurfaceLoader, CachingSurfaceLoader


load_surface = SurfaceLoader(
  resources.files(__name__).joinpath("graphics")
)

get_surface = CachingSurfaceLoader(load_surface)
