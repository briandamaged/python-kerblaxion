
from os import PathLike
from pathlib import Path
from typing import Tuple, Union, Protocol

from importlib.abc import Traversable
from weakref import WeakValueDictionary

import pygame

PathCoercible = Union[PathLike, str]

class SurfaceLoaderFunc(Protocol):
  def __call__(self,
    k1: PathCoercible,
    *rest: PathCoercible,
  )-> pygame.Surface:
    ...


class SurfaceLoader(SurfaceLoaderFunc):
  def __init__(self, root: Traversable):
    self.root = root

  def __call__(self,
    k1: PathCoercible,
    *rest: PathCoercible,
  ) -> pygame.Surface:
    target = self.root.joinpath(k1, *rest)
    with target.open("rb") as fin:
      return pygame.image.load(fin)


class CachingSurfaceLoader(SurfaceLoaderFunc):
  def __init__(self, load_surface: SurfaceLoaderFunc):
    self.__load_surface = load_surface
    self.__cache = WeakValueDictionary[Tuple[str], pygame.Surface]()

  @property
  def load_surface(self):
    return self.__load_surface

  @property
  def cache(self):
    return self.__cache

  def __call__(self,
    k1: PathCoercible,
    *rest: PathCoercible,
  ) -> pygame.Surface:
    key = Path(k1).joinpath(*rest).parts
    v = self.__cache.get(key)
    if v is None:
      v = self.__cache[key] = self.__load_surface(k1, *rest)

    return v
