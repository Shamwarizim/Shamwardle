import random

from functions.game import Wordle
from functions.solver import Pyduction

wordle = Wordle()
wordle.outputAttr()
pyduction = Pyduction(wordle)

#pyduction.guess()


##
print('GUESS COLOUR | Score | Words w/ Identical Score')
# Play the game.
for i in range(6):
    
    pyduction.guess()
    print(f'{wordle.guesses[-1]} {wordle.colouredGuesses[-1]} | S {pyduction.maxScore} | {len(pyduction.maxWords)}')
    
    if wordle.colouredGuesses[-1] == '22222':
        print(f'Pyduction got it in {i+1} guesses!')
        break
    elif i == 5 and wordle.colouredGuesses[-1] != '22222':
        print(f'Pyduction failed to get it.')
