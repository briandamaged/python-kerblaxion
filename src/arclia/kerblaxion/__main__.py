
from .game import Game
from .hero import prepare

def main():
  game = Game()
  prepare(game)
  game.run()
