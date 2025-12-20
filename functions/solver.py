import logging as log
log.basicConfig(format="[%(asctime)s] [%(filename)s/%(levelname)s]: %(message)s (Line: %(lineno)s)",
                    datefmt="%H:%M:%S",
                    level=log.DEBUG)
#DEBUG > INFO > WARNING > ERROR > CRITICAL

from functions.game import Wordle
game = Wordle()
# Attributes of game:
#   allowedWords: list
#   answer: str
#   guesses: list
#   colouredGuesses: list
#   round: int
#   humanPlayer: bool


class Pyduction:
    def __init__(self, wordle: object):
        log.debug('Ay im initialising over ere')
        pass
