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
        self.greys = []
        self.yellows = {} # In format: {'letter': [position1, position2, position5]}
        self.greens = {} # In format: as above
        self.wordle = wordle

    def guess(self, guess=None):
        wordle = self.wordle

        # MAKE THE GUESS
        if guess is None: # guess best possible guess
            self.genInfoScore(wordle.allowedWords)
            wordle.guess(random.choice(self.maxWords))
        else: # guess inputted guess (if one was inputted)
            wordle.guess(guess)

        # STORE INFO FROM THE GUESS
        colouredLetters = wordle.colouredLetters[-1]
        for position, (letter, colour) in enumerate(colouredLetters):
            # Grey
            if colour == 0:
                self.greys.append(letter)
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



    def genInfoScore(self, words: list):
#!! make it so we use a culled list for calculating letter percentage !!
        ## LETTER PERCENTAGE
        joinedLetters = ''.join(words)

        letterNums = collections.Counter(joinedLetters).most_common() #--> list of 2 item tuples

        letterPercentage = {}
        for pair in letterNums:
            percent = ( pair[1] / len(joinedLetters) ) * 100
            percent = round(percent, 2)
            letterPercentage[pair[0]] = percent
        
        ## CREATE INFO SCORE
        rankedWords = {}
        for word in words:
            # Add each letter probability (exclu doubles), UNLESS the letter is a grey.
            prob = 0
            usedLetters = []
            for letter in word:
                if (letter not in usedLetters) and (letter not in self.greys):
                    prob += letterPercentage[letter]
                    usedLetters.append(letter)
            prob = round(prob, 5)

            rankedWords[word] = prob


        # Get maximum possibles.
        self.maxScore = max(rankedWords.values())
        self.maxWords = [k for k, v in rankedWords.items() if v == self.maxScore]
        self.rankedWords = rankedWords