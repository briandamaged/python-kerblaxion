
import sys

from dataclasses import dataclass

import pygame
from pygame.locals import *

from arclia.happygame.math import Vector2Coercible

from .assets import FONTS_PATH, get_surface, MUSIC_PATH
from .hero import Hero


class Enemy(pygame.sprite.Sprite):
  def __init__(self,
    position: Vector2Coercible,
    game: "Game",
  ):
    super().__init__()
    self.game = game

    self.image = get_surface("enemy01.png")

    self.rect = self.image.get_rect(
      center = position,
    )

    self.direction = +1

    self.exploding = False
    self.explode_index = 0

    self.explosions = [
      get_surface(f"explode0{i+1}.png")
      for i in range(4)
    ]

  def destroy(self):
    self.exploding = True
    self.game.score += 1

  def update(self):
    if self.exploding:
      self.image = self.explosions[self.explode_index]
      self.explode_index += 1
      if self.explode_index >= 4:
        self.kill()
    else:
      self.rect.x += self.direction

      if self.rect.right >= 320 or self.rect.left <= 0:
        self.direction = -self.direction
        self.rect.y += 8


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

    self.visible_sprites.add(Hero(
      position = (180, 160),
      game = self,
    ))

    for x in range(16, 260, 24):
      for y in range(16, 100, 24):
        e = Enemy(
          position = (x, y),
          game = self,
        )
        self.visible_sprites.add(e)
        self.enemies.add(e)

    self.score = 0
    self.font = self.font = pygame.font.Font(FONTS_PATH / "Silkscreen-Regular.ttf", 8)

    self.life_surface = get_surface("hero", "life.png")

  @property
  def lives(self):
    return (self.score // 5) + 1

  def run(self):
    pygame.mixer.music.load(MUSIC_PATH.joinpath("level01.mp3").open())
    pygame.mixer.music.play(-1)
    while True:
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()

      keys = pygame.key.get_pressed()
      if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()

      self.visible_sprites.update()

      self.render_surface.fill(color = (0, 0, 0))
      self.visible_sprites.draw(self.render_surface)

      score_surface = self.font.render(
        f"{self.score:03d} POINTS",
        False,
        (255, 255, 255),
      )

      score_rect = score_surface.get_rect(
        center = (160, 8),
      )

      self.render_surface.blit(
        source = score_surface,
        dest = score_rect,
      )

      for life_no in range(self.lives):
        self.render_surface.blit(
          source = self.life_surface,
          dest = self.life_surface.get_rect(
            bottomright = (320, 180 - (life_no * 10))
          )
        )

      pygame.transform.scale(
        surface = self.render_surface,
        size = (1280, 720),
        dest_surface = self.display_surface,
      )

      pygame.display.update()

      self.clock.tick(self.fps)
