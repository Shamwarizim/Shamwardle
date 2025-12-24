from functions.game import Wordle
from functions.solver import Pyduction

wordle = Wordle(answer='ample')
pyduction = Pyduction(wordle)


# Play the game.
print('GUESS COLOUR | Info Score | Prob Score | Score Used | Equal Score / Total Possibles')
for i in range(6):
    pyduction.guess()
    guess = wordle.guesses[-1] 
    print(f'{guess} {wordle.colouredGuesses[-1]} | IS {pyduction.infoScores[guess]} | PS {pyduction.probScores[guess]} | {pyduction.scoreUsed} | {len(pyduction.maxInfoWords)}/{len(pyduction.possibles)}')
    
    if wordle.colouredGuesses[-1] == '22222':
        print(f'Pyduction got it in {i+1} guesses!')
        break
    elif i == 5 and wordle.colouredGuesses[-1] != '22222':
        print(f'Pyduction failed to get it. Word was {wordle.answer}.')
