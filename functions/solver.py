import logging as log
log.basicConfig(format="[%(asctime)s] [%(filename)s/%(levelname)s]: %(message)s (Line: %(lineno)s)",
                    datefmt="%H:%M:%S",
                    level=log.DEBUG)
#DEBUG > INFO > WARNING > ERROR > CRITICAL
import collections
import random


# Attributes of Wordle object:
#   allowedWords: list
#   answer: str
#   guesses: list
#   colouredGuesses: list
#   round: int
#   humanPlayer: bool


class Pyduction:
    def __init__(self, wordle: object):
        self.greys = set()
        self.yellows = {} # In format: {'letter': [position1, position2, position5]}
        self.greens = {} # In format: as above
        self.wordle = wordle
        self.possibles = wordle.allowedWords

    def guess(self, guess=None):
        wordle = self.wordle

        # MAKE THE GUESS
        # Decide best possible guess.
        if guess is None:
            self.genScores(wordle.allowedWords)
            # Final Guess Logic
            if len(wordle.guessesSet) == 5:
                guess = random.choice(self.maxProbWords)
                self.scoreUsed = 'PS'
                wordle.guess(guess)

            # Regular Guess Logic
            else:
                guess = random.choice(self.maxInfoWords)
                self.scoreUsed = 'IS'
                wordle.guess(guess)

        # OR use guess inputted to the function.
        else:
            wordle.guess(guess)
        

        # STORE INFO FROM THE GUESS
        singleWord_ColouredLetters = wordle.colouredLetters[-1]
        for position, (letter, colour) in enumerate(singleWord_ColouredLetters):
            # Grey
            if colour == 0:
                self.greys.add(letter)
            # Yellow
            elif colour == 1:
                if letter not in self.yellows:
                    self.yellows[letter] = []
                self.yellows[letter].append(position)
            # Green
            elif colour == 2:
                if letter not in self.greens:
                    self.greens[letter] = []
                self.greens[letter].append(position)



    def genScores(self, words: list):
        wordle = self.wordle

        ## POSSIBLES LIST
        newPossibles = []
        for word in self.possibles:
            possible = True

            # Greys
            for letter in self.greys:
                if letter in word:
                    possible = False
                    break
            # Yellows
            for letter, positions in self.yellows.items():
                if letter not in word:
                    possible = False
                    break
                for pos in positions:
                    if word[pos] == letter:
                        possible = False
                        break
            # Greens
            for letter, positions in self.greens.items():
                for pos in positions:
                    if word[pos] != letter:
                        possible = False
                        break
            
            if possible:
                newPossibles.append(word)

        self.possibles = newPossibles

        ## LETTER PERCENTAGE
        # Count
        letterCounts = collections.Counter() # create empty counter
        for word in self.possibles:
            letterCounts.update(word)
        #--> letterCounts: dict

        # Percentage
        total = sum(letterCounts.values())
        letterPercentage = {
            l: round((c / total) * 100, 2)
            for l, c in letterCounts.items()
        }
        
        ## CREATE SCORES
        infoScores = {}
        probScores = {}
        for word in words:
            score = 0
            # Letter Probability
            #   Add each letter probability (exclu doubles), UNLESS the letter is a grey.
            for letter in set(word):
                if (letter not in self.greys) and (letter in letterPercentage):
                    score += letterPercentage[letter]

            # Store Final Scores
            # for info (and prob) score, previously guessed words should have 0 score
            if word not in wordle.guessesSet:
                infoScores[word] = score
            else:
                infoScores[word] = 0

            #   for prob score impossible words should have 0 score as well as above prereq
            if (word in self.possibles) and (word not in wordle.guessesSet):
                probScores[word] = score
            else:
                probScores[word] = 0
        

        # Get maximum scores.
        self.maxInfoScore = max(infoScores.values())
        self.maxInfoWords = [k for k, v in infoScores.items() if v == self.maxInfoScore]
        self.maxProbScore = max(probScores.values())
        self.maxProbWords = [k for k, v in probScores.items() if v == self.maxProbScore]
        # Save raw scores too.
        self.infoScores = infoScores
        self.probScores = probScores