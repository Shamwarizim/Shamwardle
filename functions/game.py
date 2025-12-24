import logging as log
log.basicConfig(format="[%(asctime)s] [%(filename)s/%(levelname)s]: %(message)s (Line: %(lineno)s)",
                    datefmt="%H:%M:%S",
                    level=log.DEBUG)
#DEBUG > INFO > WARNING > ERROR > CRITICAL
import collections
import random
import os
currentDir = os.path.dirname(__file__)
dataPath = os.path.join(currentDir, '..', 'data')

#################################################################################

class Wordle:
    # INITIALISER
    def __init__(self, acceptedGuesses='guesses', humanPlayer=False, answer=None):
        acceptedGuessesPath = os.path.join(dataPath, f'{acceptedGuesses}.txt')
        answersPath = os.path.join(dataPath, 'answers.txt')

        with open(acceptedGuessesPath) as txt: allowedWords = txt.read().splitlines()
        with open(answersPath) as f: allowedAnswers = f.read().splitlines()

        allowedWords.extend(allowedAnswers)
        self.allowedWords = list(set(allowedWords)) # clear duplicates
        
        if answer is not None:
            self.answer = answer
        else:
            self.answer = random.choice(allowedAnswers)

        self.guesses = []
        self.guessesSet = set()
        self.colouredGuesses = []
        self.colouredLetters = []
        self.round = 0
        self.humanPlayer = humanPlayer

        if humanPlayer == True:
            self.humanLoop()

        #############################################

    # FUNCTIONS

    def humanLoop(self):
        print('''~~SHAMWARDLE~~
2 is green, 1 is yellow, 0 is grey.
You have six guesses:''')
        while self.round <= 7:
            self.guess( input('') )
    
    ##########################################################

    def guess(self, guess):
        # Invalid word
        if guess.lower() not in self.allowedWords:
            if self.humanPlayer == True:
                print('DISALLOWED WORD')
            return
        elif guess.lower() in self.guesses:
            if self.humanPlayer == True:
                print('ALREADY GUESSED WORD')
            else:
                raise Exception('You cannot guess the same word multiple times.')
            return

        # Increment round
        self.round += 1
        if self.round >= 7:
            return
        
        # Update guess list
        self.guesses.append(guess)
        self.guessesSet.add(guess)
        evaluatedGuess, colouredGuess = self.evaluate(guess)
        self.colouredGuesses.append(colouredGuess)
        if self.humanPlayer == True:
            print(colouredGuess)

        colouredLetters = [] # this is temporary to add to the list of lists
        for i in range(5):
            pair = (guess[i], int(colouredGuess[i]))
            colouredLetters.append(pair)
        self.colouredLetters.append(colouredLetters)

        

        # Check for win or loss
        total = 0
        for (letter, colour) in evaluatedGuess:
            total += colour

        if total == 10:
            if self.humanPlayer == True:
                print(f'You got the Shamwardle in {self.round} guesses!')
                self.round = 8 #any number >7 works. this just ensures the human player loop stops
        elif total != 10 and self.round == 6:
            if self.humanPlayer == True:
                print(f'''Is this what they're going to remember you for? Failing the Shamwardle?
The word was {self.answer}.
''')
                self.round = 8 #any number >7 works. this just ensures the human player loop stops
    
    ##########################################################

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