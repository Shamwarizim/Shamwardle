from functions.game import Wordle
from functions.solver import Pyduction
import statistics
import time
import datetime


trials = 1000

guessNums = []
startTime = time.time()
for i in range(trials):
    wordle = Wordle()
    pyduction = Pyduction(wordle)

    for i in range(6):
        pyduction.guess()

        if wordle.colouredGuesses[-1] == '22222':
            guessNums.append(i+1)
            break
        elif i == 5 and wordle.colouredGuesses[-1] != '22222':
            guessNums.append(7)

endTime = time.time()
elapsedTimeSecs = round(endTime - startTime, 2)
elapsedTime = datetime.timedelta(seconds=elapsedTimeSecs)


# MMM
successfulGuessNums = [guessNum for guessNum in guessNums if guessNum <= 6]
fails = len(guessNums) - len(successfulGuessNums)
failRate = f"{( fails / len(guessNums) ):.2%}"

print(f'''
Ran {len(guessNums)} trials. ( Time elapsed: {elapsedTime})
{fails} trials failed. ( {failRate} fail rate.)

INCLUSIVE OF FAILS (COUNTED AS 7)
Average of {round(statistics.mean(guessNums), 5)} guesses found.
Median of {statistics.median(guessNums)} guesses found.
Mode of {statistics.mode(guessNums)} guesses found.

EXCLUSIVE OF FAILS
Average of {round(statistics.mean(successfulGuessNums), 5)} guesses found.
Median of {statistics.median(successfulGuessNums)} guesses found.
Mode of {statistics.mode(successfulGuessNums)} guesses found.
''')