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
        self.possibles = wordle.allowedWords

    def guess(self, guess=None):
        wordle = self.wordle

        # MAKE THE GUESS
        #   Decide best possible guess.
        if guess is None:
            self.genScores(wordle.allowedWords)
            # Final Guess Logic
            if len(wordle.guesses) == 5:
                wordle.guess(random.choice(self.maxProbWords))
                self.scoreUsed = 'PS'
            # Regular Guess Logic
            else:
                wordle.guess(random.choice(self.maxInfoWords))
                self.scoreUsed = 'IS'


        #   OR use guess inputted to the function.
        else:
            wordle.guess(guess)

        # STORE INFO FROM THE GUESS
        singleWord_ColouredLetters = wordle.colouredLetters[-1]
        for position, (letter, colour) in enumerate(singleWord_ColouredLetters):
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



    def genScores(self, words: list):
        wordle = self.wordle

        for subList in wordle.colouredLetters:
        # where subList is in form [('s', 1), ('o', 0), ('a', 0), ('r', 1), ('e', 2)]
            for i, (letter, colour) in enumerate(subList):
                # GREYS
                if colour == 0:
                    # Cull words where letter in THIS position
                    self.possibles = [word for word in self.possibles if word[i] != letter]
                # YELLOWS
                if colour == 1:
                    # Cull words where letter isn't in word OR is but at this position
                    self.possibles = [word for word in self.possibles if letter in word and word[i] != letter]
                # GREENS
                if colour == 2:
                    # Cull words where letter isn't in THIS position
                    self.possibles = [word for word in self.possibles if word[i] == letter]

        ## LETTER PERCENTAGE
        joinedLetters = ''.join(self.possibles)

        letterNums = collections.Counter(joinedLetters).most_common() #--> list of 2 item tuples

        letterPercentage = {}
        for pair in letterNums:
            percent = ( pair[1] / len(joinedLetters) ) * 100
            percent = round(percent, 2)
            letterPercentage[pair[0]] = percent
        
        ## CREATE SCORES
        infoScores = {}
        probScores = {}
        for word in words:
            score = 0
            # Letter Probability
            #   Add each letter probability (exclu doubles), UNLESS the letter is a grey.
            usedLetters = []
            for letter in word:
                if (letter not in usedLetters) and (letter not in self.greys) and (letter in letterPercentage):
                    score += letterPercentage[letter]
                    usedLetters.append(letter)
            score = round(score, 5)

            # Store Final Scores
            infoScores[word] = score

            #   for probability score impossible words should have a score of 0
            if word in self.possibles:
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