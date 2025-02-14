#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ADITYA
#
# Created:     14/02/2025
# Copyright:   (c) ADITYA 2025
#-----------------------------------------------------------------------------
import random#importiing random for word guessing

name = input("What is your name? ")#starting game with user's name

print("Good Luck ! ", name)

words = ['rainbow', 'computer', 'science', 'programming',
         'python', 'mathematics', 'player', 'condition',
         'reverse', 'water', 'board', 'geeks']#list of words in future can be taken by ai

word = random.choice(words)

print("Guess the characters")

guesses = ''
turns = 12

while turns > 0:

    failed = 0

    for char in word:

        if char in guesses:
            print(char, end=" ")

        else:
            print("_")
            failed += 1

    if failed == 0:
        print("You Win")
        print("The word is: ", word)
        break

    print()
    guess = input("guess a character:")

    guesses += guess

    if guess not in word:

        turns -= 1
        print("Wrong")
        print("You have", + turns, 'more guesses')

        if turns == 0:
            print("You Loose")



