
import pygame
from pygame.locals import *

from arclia.happygame.math import Vector2Coercible
from arclia.pubsub import Publisher

from .assets import get_surface, get_sound
from .ui.score import Scoreboard
from .game import GameManager, Scene, UpdateContext

class Explosion(pygame.sprite.Sprite):
  def __init__(self,
    position: Vector2Coercible,
  ):
    super().__init__()
    self.position = pygame.Vector2(position)

    self.explode_index = 0
    self.explosions = [
      get_surface(f"explode0{i+1}.png")
      for i in range(4)
    ]

    self.started_at = pygame.time.get_ticks()

  @property
  def image(self):
    return self.explosions[self.explode_index]

  @property
  def rect(self):
    return self.image.get_rect(
      center = self.position,
    )

  def update(self, ctx: UpdateContext):
    # Update the explosion animation every 32 milliseconds
    self.explode_index = (ctx.t - self.started_at) >> 5

    if self.explode_index >= len(self.explosions):
      self.kill()


class Enemy(pygame.sprite.Sprite):
  def __init__(self,
    position: Vector2Coercible,
  ):
    super().__init__()
    self.position = pygame.Vector2(position)

    self.image = get_surface("enemy01.png")

    self.direction = +1

    self.on_destroyed = Publisher[Enemy]()

  @property
  def rect(self):
    return self.image.get_rect(
      center = self.position,
    )

  def destroy(self):
    self.on_destroyed(self)
    self.kill()

  def update(self, ctx: UpdateContext):
    self.position.x += self.direction

    r = self.rect
    if r.right >= 320 or r.left <= 0:
      self.direction = -self.direction
      self.position.y += 8


class Bullet(pygame.sprite.Sprite):
  def __init__(self, position, game):
    super().__init__()
    self.game = game

    self.image = pygame.surface.Surface(size = (4, 4))
    self.image.fill(color = (255, 255, 0))

    self.rect = self.image.get_rect(
      center = position,
    )

    self.explode_sfx = get_sound("hero-explode.wav")

  def update(self, ctx: UpdateContext):
    self.rect.y -= 4

    collisions = pygame.sprite.spritecollide(
      sprite = self,
      group = self.game.enemies,
      dokill = False,
    )

    if len(collisions) > 0:
      for c in collisions:
        c.destroy()
      self.explode_sfx.play()
      self.kill()
      return

    if self.rect.bottom < 0:
      self.kill()


class Hero(pygame.sprite.Sprite):
  def __init__(self, position, game):
    super().__init__()
    self.game = game

    self.images = [
      get_surface(f"hero/hero0{i + 1}.png")
      for i in range(4)
    ]

    self.image_index = 0

    self.rect = self.image.get_rect(
      center = position,
    )

    self.shoot_sfx = get_sound("shoot.wav")

    self.shooting = False

  @property
  def image(self):
    return self.images[self.image_index]

  def update(self, ctx: UpdateContext):
    self.image_index = (ctx.t >> 5) % 4

    pressed = pygame.key.get_pressed()
    boosted = pressed[K_LSHIFT]

    v = 2 * (2 if boosted else 1)

    if pressed[K_LEFT]:
      self.rect.x -= v

    if pressed[K_RIGHT]:
      self.rect.x += v

    if pressed[K_SPACE]:
      if not self.shooting:
        self.game.visible_sprites.add(
          Bullet(
            position = self.rect.center,
            game = self.game,
          )
        )
        self.shoot_sfx.play()
        self.shooting = True
    else:
      self.shooting = False


class GameScene(Scene):
  def __init__(self):
    self.visible_sprites = pygame.sprite.Group()
    self.player_bullets = pygame.sprite.Group()
    self.enemies = pygame.sprite.Group()

    self.scoreboard = Scoreboard()

  def update(self, ctx: UpdateContext):
    self.visible_sprites.update(ctx)

  def draw(self, surface: pygame.surface.Surface):
    surface.fill(color = (0, 0, 0))
    self.visible_sprites.draw(surface)

    surface.blit(
      self.scoreboard.image,
      dest = self.scoreboard.image.get_rect(
        topright = (320, 0),
      )
    )


def prepare():
  scene = GameScene()

  def handle_enemy_destroyed(enemy: Enemy):
    scene.scoreboard.score += 250
    explosion = Explosion(position = enemy.position)
    scene.visible_sprites.add(explosion)

  scene.visible_sprites.add(Hero(
    position = (180, 160),
    game = scene,
  ))

  for x in range(16, 260, 24):
    for y in range(16, 100, 24):
      e = Enemy(
        position = (x, y),
      )

      e.on_destroyed.add(handle_enemy_destroyed)

      scene.visible_sprites.add(e)
      scene.enemies.add(e)

  return scene
