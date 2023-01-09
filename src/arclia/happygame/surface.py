
from abc import ABC, abstractmethod
from typing import Callable, Tuple

from weakref import WeakValueDictionary
from pathlib import Path

import pygame
from pygame.surface import Surface

from arclia.quest.typing import PathCoercible


SurfaceLoaderFunc = Callable[[Tuple[str, ...]], Surface]


class AbstractSurfaceLoader(ABC):
  @abstractmethod
  def __call__(self, *key: str)-> Surface:
    ...


class FSSurfaceLoader(AbstractSurfaceLoader):
  def __init__(self, root_path: PathCoercible):
    self.__root_path = Path(root_path).resolve()

  @property
  def root_path(self):
    return self.__root_path

  def __call__(self, *key: str) -> Surface:
    full_path = self.root_path.joinpath(*key).resolve()
    if not self.root_path in full_path.parents:
      raise KeyError(f"key jailbreaks from root_path: {repr(key)}")

    return pygame.image.load(full_path)


class TransformingSurfaceLoader(AbstractSurfaceLoader):
  def __init__(self, load_surface: SurfaceLoaderFunc, transform: Callable[[Surface], Surface]):
    self.__load_surface = load_surface
    self.__transform = transform

  def __call__(self, *key: str) -> Surface:
    return self.__transform(self.__load_surface(*key))


class CachingSurfaceLoader(AbstractSurfaceLoader):
  def __init__(self, load_surface: SurfaceLoaderFunc):
    self.__load_surface = load_surface
    self.__cache = WeakValueDictionary[Tuple[str], Surface]()

  @property
  def load_surface(self):
    return self.__load_surface

  @property
  def cache(self):
    return self.__cache

  def __call__(self, *key: str):
    v = self.__cache.get(key)
    if v is None:
      v = self.__cache[key] = self.__load_surface(*key)

    return v

