import logging as log
log.basicConfig(format="[%(asctime)s] [%(filename)s/%(levelname)s]: %(message)s (Line: %(lineno)s)",
                    datefmt="%H:%M:%S",
                    level=log.DEBUG)
#DEBUG > INFO > WARNING > ERROR > CRITICAL
import collections
import random
import os
currentDir = os.path.dirname(__file__) #get current folder



## CLASS
class Wordle:
    # INITIALISER
    def __init__(self, wordFile, answer=None):
        # Create Possibles list
        wordFilePath = os.path.join(currentDir, f'{wordFile}.txt')
        answersPath = os.path.join(currentDir, 'answers.txt')

        with open(wordFilePath) as txt: allowedWords = txt.read().splitlines()
        with open(answersPath) as f: allowedAnswers = f.read().splitlines()
        allowedWords.extend(allowedAnswers)
        self.allowedWords = list(set(allowedWords)) # clear duplicates

        self.wordFile = wordFile
        
        if answer is not None:
            self.answer = answer
        else:
            self.answer = random.choice(allowedAnswers)

        self.guesses = []
        self.round = 0
    
    # FUNCTIONS
    def playerLoop(self):
        print('''~~SHAMWARDLE~~ (aka ~PY-DUCTION~)
2 is green, 1 is yellow, 0 is grey.
Make a guess:
''')
        while self.round < 6:
            self.guess( input('') )
    
    def guess(self, guess):
        # Invalid word
        if guess not in self.allowedWords:
            print('WORD NOT ALLOWED')
            return

        # Increment round
        self.round += 1
        if self.round > 6:
            print("You failed the Wordle D:")
            return
        
        # Update guess list
        self.guesses.append(guess)
        evaluatedGuess, colouredGuess = self.evaluate(guess)
        print(colouredGuess)

        # Check for win
        total = 0
        for (letter, colour) in evaluatedGuess:
            total += colour
        if total == 10:
            print(f'You got the Wordle in {self.round} guesses!')

        return evaluatedGuess, colouredGuess

    # EVALUATE
    def evaluate(self, guess):
        answer = self.answer
        
        aLetters = list(answer)
        aCounts = collections.Counter(aLetters)
        gLetters = list(guess)
        evaluatedGuess = []

        # GREENS - Loop 1
        for i, letter in enumerate(gLetters):
            if letter == aLetters[i]:
                evaluatedGuess.append([letter, 2])
                aCounts[letter] -= 1
            else:
                evaluatedGuess.append([letter, None])

        # YELLOWS & GREYS - Loop 2
        for i, (letter, colour) in enumerate(evaluatedGuess):
            if colour is None:
                # Yellows
                if aCounts[letter] > 0:
                    evaluatedGuess[i] = [letter, 1]
                    aCounts[letter] -= 1
                # Greys
                else:
                    evaluatedGuess[i] = [letter, 0]

        # Colours
        colouredGuess = ''
        for (letter, colour) in evaluatedGuess:
            colouredGuess += str(colour)

        return evaluatedGuess, colouredGuess

    # DEBUGS
    def outputAttr(self):
        for variable in vars(self):
            value = vars(self)[variable]
            print(f'{variable} = {value}') # cant use log cos it wont squeeze text


game = Wordle('guesses')
game.playerLoop()