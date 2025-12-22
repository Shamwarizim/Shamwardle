from functions.game import Wordle
from functions.solver import Pyduction

wordle = Wordle()
pyduction = Pyduction(wordle)


# Play the game.
print('GUESS COLOUR | Score | Equal Score / Total Possibles')
for i in range(6):
    pyduction.guess()
    print(f'{wordle.guesses[-1]} {wordle.colouredGuesses[-1]} | S {pyduction.maxScore} | {len(pyduction.maxWords)}/{len(pyduction.possibles)}')
    
    if wordle.colouredGuesses[-1] == '22222':
        print(f'Pyduction got it in {i+1} guesses!')
        break
    elif i == 5 and wordle.colouredGuesses[-1] != '22222':
        print(f'Pyduction failed to get it. Word was {wordle.answer}.')
